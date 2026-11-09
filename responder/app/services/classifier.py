ALLOWED_ACTIONS = {"DISABLE_DEMO_FAILURE_MODE"}


def classify_alert(alert: dict) -> dict:
    labels = alert.get("labels") or {}
    alertname = labels.get("alertname", "")
    annotations = alert.get("annotations") or {}

    if alertname == "ServiceRequestSubmissionUserImpact" or labels.get(
        "journey"
    ) == "service_request_submission":
        return {
            "incident_type": "DEMO_FAILURE_MODE",
            "root_cause": "Controlled demo failure mode appears enabled; submissions returning failures.",
            "action": "DISABLE_DEMO_FAILURE_MODE",
            "severity": "high",
            "summary": annotations.get("summary", "User-impacting submission failures detected"),
        }

    return {
        "incident_type": "UNKNOWN",
        "root_cause": "Unrecognized alert; escalation required",
        "action": None,
        "severity": "medium",
        "summary": annotations.get("summary", "Unrecognized alert"),
    }


def is_action_allowed(action: str | None) -> bool:
    return action in ALLOWED_ACTIONS
