from sqlalchemy.orm import Session

from app.models.entities import AuditEvent
from app.observability.tracing import current_trace_id


def record_audit(
    db: Session,
    *,
    event_type: str,
    entity_id: str | None = None,
    metadata: dict | None = None,
) -> AuditEvent:
    event = AuditEvent(
        event_type=event_type,
        entity_id=entity_id,
        trace_id=current_trace_id(),
        event_metadata=metadata or {},
    )
    db.add(event)
    db.flush()
    return event
