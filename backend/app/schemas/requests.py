from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.entities import (
    IncidentSeverity,
    IncidentStatus,
    Priority,
    RemediationStatus,
    RequestStatus,
    ServiceCategory,
)


class ServiceRequestCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=120)
    customer_email: EmailStr
    service_category: ServiceCategory
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5, max_length=4000)
    priority: Priority


class ServiceRequestStatusUpdate(BaseModel):
    status: RequestStatus


class ServiceRequestRead(BaseModel):
    id: UUID
    customer_name: str
    customer_email: EmailStr
    service_category: ServiceCategory
    title: str
    description: str
    priority: Priority
    status: RequestStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RemediationRead(BaseModel):
    id: UUID
    action_type: str
    status: RemediationStatus
    started_at: datetime
    finished_at: datetime | None
    diagnostic_summary: str | None
    verification_result: str | None

    model_config = {"from_attributes": True}


class IncidentRead(BaseModel):
    id: UUID
    alert_fingerprint: str
    incident_type: str
    severity: IncidentSeverity
    status: IncidentStatus
    detected_at: datetime
    acknowledged_at: datetime | None
    resolved_at: datetime | None
    root_cause: str | None
    recovery_verified: bool
    remediations: list[RemediationRead] = []

    model_config = {"from_attributes": True}


class ReliabilitySummary(BaseModel):
    total_requests: int
    open_requests: int
    in_progress_requests: int
    completed_requests: int
    submission_success_count: int
    submission_failure_count: int
    submission_success_rate: float
    active_incidents: int
    recent_incidents: list[IncidentRead]


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None
    trace_id: str | None = None
