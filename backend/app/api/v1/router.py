import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import require_admin, require_recovery, require_webhook
from app.models.entities import IncidentSeverity, IncidentStatus
from app.schemas.internal import (
    EscalateIncidentRequest,
    IncidentUpsertRequest,
    IncidentUpsertResponse,
    RemediationCreateRequest,
    ResolveIncidentRequest,
)
from app.schemas.requests import (
    IncidentRead,
    ReliabilitySummary,
    RemediationRead,
    ServiceRequestCreate,
    ServiceRequestRead,
    ServiceRequestStatusUpdate,
)
from app.services import incident_service, request_service
from app.services.audit import record_audit
from app.services.settings_service import is_demo_failure_enabled, set_demo_failure

router = APIRouter(prefix="/api/v1")


@router.get("/requests", response_model=list[ServiceRequestRead])
def list_requests(db: Annotated[Session, Depends(get_db)]) -> list[ServiceRequestRead]:
    return request_service.list_service_requests(db)


@router.post(
    "/requests",
    response_model=ServiceRequestRead,
    status_code=status.HTTP_201_CREATED,
)
def create_request(
    payload: ServiceRequestCreate, db: Annotated[Session, Depends(get_db)]
) -> ServiceRequestRead:
    return request_service.create_service_request(db, payload)


@router.get("/requests/{request_id}", response_model=ServiceRequestRead)
def get_request(
    request_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
) -> ServiceRequestRead:
    return request_service.get_service_request(db, request_id)


@router.patch("/requests/{request_id}/status", response_model=ServiceRequestRead)
def patch_status(
    request_id: uuid.UUID,
    payload: ServiceRequestStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_admin)],
) -> ServiceRequestRead:
    return request_service.update_request_status(db, request_id, payload.status)


@router.get("/incidents", response_model=list[IncidentRead])
def list_incidents(db: Annotated[Session, Depends(get_db)]) -> list[IncidentRead]:
    return incident_service.list_incidents(db)


@router.get("/incidents/{incident_id}", response_model=IncidentRead)
def get_incident(
    incident_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
) -> IncidentRead:
    return incident_service.get_incident(db, incident_id)


@router.get("/reliability/summary", response_model=ReliabilitySummary)
def reliability_summary(db: Annotated[Session, Depends(get_db)]) -> ReliabilitySummary:
    counts = request_service.request_counts(db)
    success, failure = incident_service.submission_stats_from_audit(db)
    total_attempts = success + failure
    rate = (success / total_attempts) if total_attempts else 1.0
    incidents = incident_service.list_incidents(db, limit=10)
    active = sum(1 for i in incidents if i.status != IncidentStatus.RESOLVED)
    return ReliabilitySummary(
        total_requests=counts["total_requests"],
        open_requests=counts["open_requests"],
        in_progress_requests=counts["in_progress_requests"],
        completed_requests=counts["completed_requests"],
        submission_success_count=success,
        submission_failure_count=failure,
        submission_success_rate=round(rate, 4),
        active_incidents=active,
        recent_incidents=incidents,
    )


@router.post("/demo/failure/enable")
def enable_demo_failure(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_admin)],
) -> dict:
    settings = get_settings()
    if not settings.demo_mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Demo mode is disabled in this environment",
        )
    set_demo_failure(db, True)
    record_audit(db, event_type="demo_failure_enabled", metadata={"source": "admin"})
    db.commit()
    return {"demo_failure_mode_enabled": True}


@router.post("/demo/failure/disable")
def disable_demo_failure(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_admin)],
) -> dict:
    set_demo_failure(db, False)
    record_audit(db, event_type="demo_failure_disabled", metadata={"source": "admin"})
    db.commit()
    return {"demo_failure_mode_enabled": False}


@router.get("/demo/failure/status")
def demo_failure_status(db: Annotated[Session, Depends(get_db)]) -> dict:
    return {
        "demo_mode": get_settings().demo_mode,
        "demo_failure_mode_enabled": is_demo_failure_enabled(db),
    }


@router.post("/internal/recovery/disable-demo-failure")
def internal_disable_demo_failure(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_recovery)],
) -> dict:
    set_demo_failure(db, False)
    record_audit(
        db, event_type="demo_failure_disabled", metadata={"source": "internal_recovery"}
    )
    db.commit()
    return {"demo_failure_mode_enabled": False, "action": "DISABLE_DEMO_FAILURE_MODE"}


@router.post("/alerts/webhook")
def alerts_webhook(
    payload: dict,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_webhook)],
) -> dict:
    """Optional backend intake; primary path is the responder service."""
    alerts = payload.get("alerts") or []
    created = 0
    for alert in alerts:
        fingerprint = alert.get("fingerprint") or alert.get("labels", {}).get(
            "alertname", "unknown"
        )
        _, was_created = incident_service.upsert_incident_from_alert(
            db,
            fingerprint=str(fingerprint),
            incident_type=alert.get("labels", {}).get("alertname", "unknown"),
            severity=IncidentSeverity.HIGH,
            root_cause="alertmanager_webhook",
        )
        if was_created:
            created += 1
    return {"received": len(alerts), "created": created}


@router.post("/internal/incidents/upsert", response_model=IncidentUpsertResponse)
def internal_upsert_incident(
    payload: IncidentUpsertRequest,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_recovery)],
) -> IncidentUpsertResponse:
    incident, created = incident_service.upsert_incident_from_alert(
        db,
        fingerprint=payload.fingerprint,
        incident_type=payload.incident_type,
        severity=payload.severity,
        root_cause=payload.root_cause,
    )
    return IncidentUpsertResponse(id=incident.id, created=created, status=incident.status.value)


@router.post("/internal/incidents/{incident_id}/remediations", response_model=RemediationRead)
def internal_add_remediation(
    incident_id: uuid.UUID,
    payload: RemediationCreateRequest,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_recovery)],
) -> RemediationRead:
    incident = incident_service.get_incident(db, incident_id)
    return incident_service.add_remediation(
        db,
        incident=incident,
        action_type=payload.action_type,
        status_value=payload.status,
        diagnostic_summary=payload.diagnostic_summary,
        verification_result=payload.verification_result,
    )


@router.post("/internal/incidents/{incident_id}/resolve", response_model=IncidentRead)
def internal_resolve_incident(
    incident_id: uuid.UUID,
    payload: ResolveIncidentRequest,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_recovery)],
) -> IncidentRead:
    incident = incident_service.get_incident(db, incident_id)
    return incident_service.mark_incident_resolved(
        db, incident, verified=payload.recovery_verified
    )


@router.post("/internal/incidents/{incident_id}/escalate", response_model=IncidentRead)
def internal_escalate_incident(
    incident_id: uuid.UUID,
    payload: EscalateIncidentRequest,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(require_recovery)],
) -> IncidentRead:
    incident = incident_service.get_incident(db, incident_id)
    return incident_service.mark_incident_escalated(db, incident, payload.reason)
