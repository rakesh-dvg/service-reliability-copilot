from uuid import UUID

from pydantic import BaseModel, Field

from app.models.entities import IncidentSeverity, RemediationStatus


class IncidentUpsertRequest(BaseModel):
    fingerprint: str = Field(min_length=1, max_length=255)
    incident_type: str
    severity: IncidentSeverity = IncidentSeverity.HIGH
    root_cause: str | None = None


class RemediationCreateRequest(BaseModel):
    action_type: str
    status: RemediationStatus
    diagnostic_summary: str | None = None
    verification_result: str | None = None


class ResolveIncidentRequest(BaseModel):
    recovery_verified: bool = False


class EscalateIncidentRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=1000)


class IncidentUpsertResponse(BaseModel):
    id: UUID
    created: bool
    status: str
