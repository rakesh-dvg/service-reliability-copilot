import time
from typing import Any

import httpx

from app.config import get_settings
from app.logging_setup import get_logger
from app.services.classifier import is_action_allowed

logger = get_logger(__name__)


class RemediationError(Exception):
    pass


def gather_diagnostics(client: httpx.Client) -> dict[str, Any]:
    settings = get_settings()
    status_resp = client.get(f"{settings.backend_base_url}/api/v1/demo/failure/status", timeout=5.0)
    health = client.get(f"{settings.backend_base_url}/health", timeout=5.0)
    return {
        "backend_health": health.json() if health.status_code == 200 else {"status": "error"},
        "demo_failure_status": status_resp.json() if status_resp.status_code == 200 else {},
    }


def execute_allowlisted_action(client: httpx.Client, action: str) -> dict[str, Any]:
    if not is_action_allowed(action):
        raise RemediationError(f"Action not allowlisted: {action}")

    settings = get_settings()
    if action == "DISABLE_DEMO_FAILURE_MODE":
        resp = client.post(
            f"{settings.backend_base_url}/api/v1/internal/recovery/disable-demo-failure",
            headers={"Authorization": f"Bearer {settings.recovery_api_token}"},
            timeout=10.0,
        )
        if resp.status_code >= 400:
            raise RemediationError(f"Recovery API failed: {resp.status_code}")
        return resp.json()

    raise RemediationError(f"No executor for action: {action}")


def verify_submission_journey(client: httpx.Client) -> dict[str, Any]:
    settings = get_settings()
    payload = {
        "customer_name": "Synthetic Probe",
        "customer_email": "synthetic.probe@example.com",
        "service_category": "General Service",
        "title": "Synthetic recovery verification",
        "description": "Automated post-remediation verification request.",
        "priority": "medium",
    }
    resp = client.post(
        f"{settings.backend_base_url}/api/v1/requests",
        json=payload,
        timeout=settings.verification_timeout_seconds,
    )
    if resp.status_code != 201:
        return {"ok": False, "status_code": resp.status_code, "detail": resp.text[:300]}

    body = resp.json()
    get_resp = client.get(
        f"{settings.backend_base_url}/api/v1/requests/{body['id']}",
        timeout=settings.verification_timeout_seconds,
    )
    return {
        "ok": get_resp.status_code == 200,
        "status_code": resp.status_code,
        "persisted": get_resp.status_code == 200,
        "request_id": body.get("id"),
    }


def optional_groq_explanation(diagnosis: dict[str, Any]) -> str | None:
    settings = get_settings()
    if not settings.groq_enabled or not settings.groq_api_key:
        return None
    # Narrative only — never executed as code/commands.
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.groq_api_key}"},
                json={
                    "model": settings.groq_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "Explain the incident in plain language for an on-call engineer. "
                                "Do not propose shell commands or infrastructure changes."
                            ),
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Incident type: {diagnosis.get('incident_type')}. "
                                f"Root cause: {diagnosis.get('root_cause')}. "
                                f"Action taken (allowlisted): {diagnosis.get('action')}."
                            ),
                        },
                    ],
                },
            )
            if resp.status_code >= 400:
                logger.warning("groq_explanation_failed", extra={"status_code": resp.status_code})
                return None
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except Exception:
        logger.exception("groq_explanation_exception")
        return None


def sleep_backoff(attempt: int) -> None:
    time.sleep(min(2 * attempt, 5))
