from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

from app.config import get_settings
from app.logging_setup import configure_logging, get_logger
from app.services.handler import handle_alertmanager_payload

configure_logging()
logger = get_logger(__name__)
settings = get_settings()

app = FastAPI(title="Service Reliability Copilot Responder", version="1.0.0")

ALERTS_RECEIVED = Counter(
    "responder_alerts_received_total",
    "Alertmanager webhook payloads received",
)


def require_webhook(authorization: str | None = Header(default=None)) -> None:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    if token != settings.alert_webhook_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook token")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/webhook/alertmanager")
def alertmanager_webhook(
    payload: dict,
    _: None = Depends(require_webhook),
) -> JSONResponse:
    ALERTS_RECEIVED.inc()
    logger.info("alertmanager_webhook_received", extra={"alert_count": len(payload.get("alerts") or [])})
    result = handle_alertmanager_payload(payload)
    return JSONResponse(content=result)
