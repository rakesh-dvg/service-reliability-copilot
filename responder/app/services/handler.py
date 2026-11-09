import time
from threading import Lock
from typing import Any

import httpx

from app.config import get_settings
from app.logging_setup import get_logger
from app.services.classifier import classify_alert, is_action_allowed
from app.services.remediation import (
    RemediationError,
    execute_allowlisted_action,
    gather_diagnostics,
    optional_groq_explanation,
    sleep_backoff,
    verify_submission_journey,
)

logger = get_logger(__name__)

_fingerprint_state: dict[str, dict[str, Any]] = {}
_lock = Lock()


def _auth_headers() -> dict[str, str]:
    settings = get_settings()
    return {"Authorization": f"Bearer {settings.recovery_api_token}"}


def _should_skip(fingerprint: str) -> tuple[bool, str]:
    settings = get_settings()
    with _lock:
        state = _fingerprint_state.get(fingerprint)
        if not state:
            return False, ""
        if state.get("resolved"):
            return True, "already_resolved"
        last = state.get("last_attempt_at", 0)
        attempts = state.get("attempts", 0)
        if attempts >= settings.max_remediation_attempts:
            return True, "max_attempts_reached"
        if time.time() - last < settings.remediation_cooldown_seconds:
            return True, "cooldown_active"
        return False, ""


def _mark_attempt(fingerprint: str, *, resolved: bool = False) -> None:
    with _lock:
        state = _fingerprint_state.setdefault(fingerprint, {"attempts": 0, "resolved": False})
        state["attempts"] = int(state.get("attempts", 0)) + 1
        state["last_attempt_at"] = time.time()
        if resolved:
            state["resolved"] = True


def handle_alertmanager_payload(payload: dict) -> dict[str, Any]:
    settings = get_settings()
    alerts = payload.get("alerts") or []
    results = []

    with httpx.Client() as client:
        for alert in alerts:
            if alert.get("status") == "resolved":
                results.append({"fingerprint": alert.get("fingerprint"), "status": "ignored_resolved"})
                continue

            fingerprint = str(alert.get("fingerprint") or "unknown")
            skip, reason = _should_skip(fingerprint)
            if skip:
                logger.info(
                    "remediation_skipped",
                    extra={"fingerprint": fingerprint, "reason": reason},
                )
                results.append({"fingerprint": fingerprint, "status": "skipped", "reason": reason})
                continue

            diagnosis = classify_alert(alert)
            upsert = client.post(
                f"{settings.backend_base_url}/api/v1/internal/incidents/upsert",
                headers=_auth_headers(),
                json={
                    "fingerprint": fingerprint,
                    "incident_type": diagnosis["incident_type"],
                    "severity": diagnosis["severity"],
                    "root_cause": diagnosis["root_cause"],
                },
                timeout=10.0,
            )
            upsert.raise_for_status()
            incident = upsert.json()
            incident_id = incident["id"]

            if not incident.get("created", True) and incident.get("status") == "resolved":
                results.append(
                    {
                        "fingerprint": fingerprint,
                        "status": "already_resolved_remote",
                        "incident_id": incident_id,
                    }
                )
                continue

            diagnostics = gather_diagnostics(client)
            action = diagnosis.get("action")
            explanation = optional_groq_explanation(diagnosis)

            if not is_action_allowed(action):
                client.post(
                    f"{settings.backend_base_url}/api/v1/internal/incidents/{incident_id}/escalate",
                    headers=_auth_headers(),
                    json={"reason": "No allowlisted action for alert classification"},
                    timeout=10.0,
                )
                _mark_attempt(fingerprint)
                results.append(
                    {
                        "fingerprint": fingerprint,
                        "status": "escalated",
                        "incident_id": incident_id,
                    }
                )
                continue

            success = False
            verification: dict[str, Any] = {}
            last_error = None
            for attempt in range(1, settings.max_remediation_attempts + 1):
                try:
                    execute_allowlisted_action(client, action)
                    verification = verify_submission_journey(client)
                    if verification.get("ok"):
                        success = True
                        break
                    last_error = f"verification_failed:{verification}"
                except RemediationError as exc:
                    last_error = str(exc)
                sleep_backoff(attempt)

            _mark_attempt(fingerprint, resolved=success)

            client.post(
                f"{settings.backend_base_url}/api/v1/internal/incidents/{incident_id}/remediations",
                headers=_auth_headers(),
                json={
                    "action_type": action,
                    "status": "succeeded" if success else "failed",
                    "diagnostic_summary": str(
                        {
                            "diagnosis": diagnosis,
                            "diagnostics": diagnostics,
                            "groq_explanation": explanation,
                            "error": last_error,
                        }
                    )[:4000],
                    "verification_result": str(verification)[:2000],
                },
                timeout=10.0,
            )

            if success:
                client.post(
                    f"{settings.backend_base_url}/api/v1/internal/incidents/{incident_id}/resolve",
                    headers=_auth_headers(),
                    json={"recovery_verified": True},
                    timeout=10.0,
                )
                results.append(
                    {
                        "fingerprint": fingerprint,
                        "status": "resolved",
                        "incident_id": incident_id,
                        "action": action,
                    }
                )
            else:
                client.post(
                    f"{settings.backend_base_url}/api/v1/internal/incidents/{incident_id}/escalate",
                    headers=_auth_headers(),
                    json={"reason": last_error or "remediation_failed"},
                    timeout=10.0,
                )
                results.append(
                    {
                        "fingerprint": fingerprint,
                        "status": "escalated",
                        "incident_id": incident_id,
                        "error": last_error,
                    }
                )

    return {"processed": len(results), "results": results}
