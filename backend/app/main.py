import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import text

from app.api.v1.router import router as v1_router
from app.core.config import get_settings
from app.core.database import SessionLocal, engine
from app.observability.logging import configure_logging, get_logger
from app.observability.tracing import current_trace_id, setup_tracing
from app.services.settings_service import set_setting

configure_logging()
logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Ensure default runtime setting exists after migrations
    db = SessionLocal()
    try:
        set_setting(db, "demo_failure_mode_enabled", "false")
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("startup_runtime_settings_init_failed")
    finally:
        db.close()
    yield


app = FastAPI(
    title="Service Reliability Copilot API",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    trace_id = current_trace_id()
    response.headers["X-Request-Id"] = request_id
    if trace_id:
        response.headers["X-Trace-Id"] = trace_id
    logger.info(
        "http_request",
        extra={
            "service_name": settings.app_name,
            "request_id": request_id,
            "trace_id": trace_id,
            "route": request.url.path,
            "response_status": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_exception", extra={"route": request.url.path})
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "internal_error",
            "trace_id": current_trace_id(),
        },
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name}


@app.get("/ready")
def ready():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "detail": str(exc.__class__.__name__)},
        )


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(v1_router)
setup_tracing(app)
