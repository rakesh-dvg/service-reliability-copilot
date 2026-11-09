import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.entities import (
    AuditEvent,
    Incident,
    IncidentSeverity,
    IncidentStatus,
    RemediationAction,
    RemediationStatus,
)
from app.observability.metrics import (
    ACTIVE_INCIDENTS,
    REMEDIATION_ATTEMPTS_TOTAL,
    REMEDIATION_SUCCESS_TOTAL,
)
from app.services.audit import record_audit


def refresh_active_incidents_gauge(db: Session) -> None:
    count = (
        db.scalar(
            select(func.count())
            .select_from(Incident)
            .where(Incident.status.not_in([IncidentStatus.RESOLVED]))
        )
        or 0
    )
    ACTIVE_INCIDENTS.set(count)


def list_incidents(db: Session, limit: int = 50) -> list[Incident]:
    stmt = (
        select(Incident)
        .options(selectinload(Incident.remediations))
        .order_by(Incident.detected_at.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def get_incident(db: Session, incident_id: uuid.UUID) -> Incident:
    stmt = (
        select(Incident)
        .options(selectinload(Incident.remediations))
        .where(Incident.id == incident_id)
    )
    entity = db.scalar(stmt)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return entity


def upsert_incident_from_alert(
    db: Session,
    *,
    fingerprint: str,
    incident_type: str,
    severity: IncidentSeverity,
    root_cause: str | None = None,
) -> tuple[Incident, bool]:
    """Return (incident, created)."""
    existing = db.scalar(select(Incident).where(Incident.alert_fingerprint == fingerprint))
    if existing is not None:
        record_audit(
            db,
            event_type="incident_alert_deduplicated",
            entity_id=str(existing.id),
            metadata={"fingerprint": fingerprint},
        )
        db.commit()
        db.refresh(existing)
        return existing, False

    incident = Incident(
        id=uuid.uuid4(),
        alert_fingerprint=fingerprint,
        incident_type=incident_type,
        severity=severity,
        status=IncidentStatus.DETECTED,
        root_cause=root_cause,
        recovery_verified=False,
    )
    db.add(incident)
    record_audit(
        db,
        event_type="incident_created",
        entity_id=str(incident.id),
        metadata={"fingerprint": fingerprint, "incident_type": incident_type},
    )
    db.commit()
    db.refresh(incident)
    refresh_active_incidents_gauge(db)
    return incident, True


def add_remediation(
    db: Session,
    *,
    incident: Incident,
    action_type: str,
    status_value: RemediationStatus,
    diagnostic_summary: str | None = None,
    verification_result: str | None = None,
) -> RemediationAction:
    REMEDIATION_ATTEMPTS_TOTAL.labels(action_type=action_type).inc()
    action = RemediationAction(
        id=uuid.uuid4(),
        incident_id=incident.id,
        action_type=action_type,
        status=status_value,
        diagnostic_summary=diagnostic_summary,
        verification_result=verification_result,
        finished_at=datetime.now(UTC)
        if status_value != RemediationStatus.STARTED
        else None,
    )
    db.add(action)
    if status_value == RemediationStatus.SUCCEEDED:
        REMEDIATION_SUCCESS_TOTAL.labels(action_type=action_type).inc()
    record_audit(
        db,
        event_type="remediation_recorded",
        entity_id=str(incident.id),
        metadata={"action_type": action_type, "status": status_value.value},
    )
    db.commit()
    db.refresh(action)
    return action


def mark_incident_resolved(db: Session, incident: Incident, *, verified: bool) -> Incident:
    incident.status = IncidentStatus.RESOLVED
    incident.resolved_at = datetime.now(UTC)
    incident.recovery_verified = verified
    record_audit(
        db,
        event_type="incident_resolved",
        entity_id=str(incident.id),
        metadata={"recovery_verified": verified},
    )
    db.commit()
    db.refresh(incident)
    refresh_active_incidents_gauge(db)
    return incident


def mark_incident_escalated(db: Session, incident: Incident, reason: str) -> Incident:
    incident.status = IncidentStatus.ESCALATED
    record_audit(
        db,
        event_type="incident_escalated",
        entity_id=str(incident.id),
        metadata={"reason": reason},
    )
    db.commit()
    db.refresh(incident)
    refresh_active_incidents_gauge(db)
    return incident


def submission_stats_from_audit(db: Session) -> tuple[int, int]:
    success = (
        db.scalar(
            select(func.count())
            .select_from(AuditEvent)
            .where(AuditEvent.event_type == "service_request_created")
        )
        or 0
    )
    failure = (
        db.scalar(
            select(func.count())
            .select_from(AuditEvent)
            .where(AuditEvent.event_type == "service_request_submission_failed")
        )
        or 0
    )
    return int(success), int(failure)
