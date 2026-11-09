import time
import uuid

from fastapi import HTTPException, status
from opentelemetry import trace
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import RequestStatus, ServiceRequest
from app.observability.logging import get_logger
from app.observability.metrics import (
    SERVICE_REQUEST_SUBMISSION_DURATION_SECONDS,
    SERVICE_REQUEST_SUBMISSION_FAILURES_TOTAL,
    SERVICE_REQUEST_SUBMISSIONS_TOTAL,
)
from app.schemas.requests import ServiceRequestCreate
from app.services.audit import record_audit
from app.services.settings_service import is_demo_failure_enabled
from app.services.status_machine import can_transition

logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)


def create_service_request(db: Session, payload: ServiceRequestCreate) -> ServiceRequest:
    started = time.perf_counter()
    with tracer.start_as_current_span("validate_service_request"):
        # Pydantic already validated; span retained for journey visibility
        pass

    if is_demo_failure_enabled(db):
        SERVICE_REQUEST_SUBMISSIONS_TOTAL.labels(result="failure").inc()
        SERVICE_REQUEST_SUBMISSION_FAILURES_TOTAL.labels(reason="demo_failure_mode").inc()
        SERVICE_REQUEST_SUBMISSION_DURATION_SECONDS.observe(time.perf_counter() - started)
        record_audit(
            db,
            event_type="service_request_submission_failed",
            metadata={"reason": "demo_failure_mode"},
        )
        db.commit()
        logger.warning(
            "service_request_submission_failed",
            extra={
                "service_name": "src-backend",
                "route": "/api/v1/requests",
                "response_status": 503,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable (controlled demo failure mode)",
        )

    with tracer.start_as_current_span("persist_service_request"):
        entity = ServiceRequest(
            id=uuid.uuid4(),
            customer_name=payload.customer_name,
            customer_email=str(payload.customer_email),
            service_category=payload.service_category,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=RequestStatus.OPEN,
        )
        db.add(entity)
        record_audit(
            db,
            event_type="service_request_created",
            entity_id=str(entity.id),
            metadata={"priority": payload.priority.value},
        )
        db.commit()
        db.refresh(entity)

    duration = time.perf_counter() - started
    SERVICE_REQUEST_SUBMISSIONS_TOTAL.labels(result="success").inc()
    SERVICE_REQUEST_SUBMISSION_DURATION_SECONDS.observe(duration)
    logger.info(
        "service_request_submission_succeeded",
        extra={
            "service_name": "src-backend",
            "route": "/api/v1/requests",
            "response_status": 201,
            "duration_ms": round(duration * 1000, 2),
            "request_id": str(entity.id),
        },
    )
    return entity


def list_service_requests(db: Session, limit: int = 50) -> list[ServiceRequest]:
    stmt = select(ServiceRequest).order_by(ServiceRequest.created_at.desc()).limit(limit)
    return list(db.scalars(stmt).all())


def get_service_request(db: Session, request_id: uuid.UUID) -> ServiceRequest:
    entity = db.get(ServiceRequest, request_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return entity


def update_request_status(
    db: Session, request_id: uuid.UUID, new_status: RequestStatus
) -> ServiceRequest:
    entity = get_service_request(db, request_id)
    if not can_transition(entity.status, new_status):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status transition from {entity.status.value} to {new_status.value}",
        )
    entity.status = new_status
    record_audit(
        db,
        event_type="service_request_status_updated",
        entity_id=str(entity.id),
        metadata={"status": new_status.value},
    )
    db.commit()
    db.refresh(entity)
    return entity


def request_counts(db: Session) -> dict[str, int]:
    total = db.scalar(select(func.count()).select_from(ServiceRequest)) or 0
    open_count = (
        db.scalar(
            select(func.count()).select_from(ServiceRequest).where(
                ServiceRequest.status == RequestStatus.OPEN
            )
        )
        or 0
    )
    in_progress = (
        db.scalar(
            select(func.count()).select_from(ServiceRequest).where(
                ServiceRequest.status == RequestStatus.IN_PROGRESS
            )
        )
        or 0
    )
    completed = (
        db.scalar(
            select(func.count()).select_from(ServiceRequest).where(
                ServiceRequest.status == RequestStatus.COMPLETED
            )
        )
        or 0
    )
    return {
        "total_requests": total,
        "open_requests": open_count,
        "in_progress_requests": in_progress,
        "completed_requests": completed,
    }
