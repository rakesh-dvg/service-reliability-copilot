from app.services.classifier import classify_alert, is_action_allowed


def test_classify_user_impact_alert():
    alert = {
        "labels": {
            "alertname": "ServiceRequestSubmissionUserImpact",
            "journey": "service_request_submission",
        },
        "annotations": {"summary": "Submissions failing"},
    }
    result = classify_alert(alert)
    assert result["incident_type"] == "DEMO_FAILURE_MODE"
    assert result["action"] == "DISABLE_DEMO_FAILURE_MODE"
    assert is_action_allowed(result["action"])


def test_unknown_alert_escalates():
    result = classify_alert({"labels": {"alertname": "DiskAlmostFull"}})
    assert result["action"] is None
    assert not is_action_allowed(result["action"])


def test_allowlist_rejects_arbitrary_action():
    assert not is_action_allowed("DELETE_DATABASE")
    assert not is_action_allowed("rm -rf /")
