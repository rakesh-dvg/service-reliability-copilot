from app.models.entities import RequestStatus

ALLOWED_TRANSITIONS: dict[RequestStatus, set[RequestStatus]] = {
    RequestStatus.OPEN: {RequestStatus.IN_PROGRESS, RequestStatus.CANCELLED},
    RequestStatus.IN_PROGRESS: {RequestStatus.COMPLETED, RequestStatus.CANCELLED},
    RequestStatus.COMPLETED: set(),
    RequestStatus.CANCELLED: set(),
}


def can_transition(current: RequestStatus, new_status: RequestStatus) -> bool:
    if current == new_status:
        return True
    return new_status in ALLOWED_TRANSITIONS.get(current, set())
