from app.models.entities import RequestStatus
from app.services.status_machine import can_transition


def test_allowed_transitions():
    assert can_transition(RequestStatus.OPEN, RequestStatus.IN_PROGRESS)
    assert can_transition(RequestStatus.IN_PROGRESS, RequestStatus.COMPLETED)
    assert can_transition(RequestStatus.OPEN, RequestStatus.CANCELLED)


def test_disallowed_transitions():
    assert not can_transition(RequestStatus.COMPLETED, RequestStatus.OPEN)
    assert not can_transition(RequestStatus.CANCELLED, RequestStatus.IN_PROGRESS)
    assert not can_transition(RequestStatus.OPEN, RequestStatus.COMPLETED)
