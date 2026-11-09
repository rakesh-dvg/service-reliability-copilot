from fastapi import Header, HTTPException, status

from app.core.config import get_settings


def _extract_bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip()


def require_admin(authorization: str | None = Header(default=None)) -> None:
    settings = get_settings()
    token = _extract_bearer(authorization)
    if token != settings.admin_api_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")


def require_recovery(authorization: str | None = Header(default=None)) -> None:
    settings = get_settings()
    token = _extract_bearer(authorization)
    if token not in {settings.recovery_api_token, settings.admin_api_token}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid recovery token"
        )


def require_webhook(authorization: str | None = Header(default=None)) -> None:
    settings = get_settings()
    token = _extract_bearer(authorization)
    if token != settings.alert_webhook_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook token"
        )
