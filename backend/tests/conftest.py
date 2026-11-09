import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Force deterministic settings before app import
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("ENABLE_OTEL", "false")
os.environ.setdefault("DEMO_MODE", "true")
os.environ.setdefault("ADMIN_API_TOKEN", "test-admin-token")
os.environ.setdefault("RECOVERY_API_TOKEN", "test-recovery-token")
os.environ.setdefault("ALERT_WEBHOOK_TOKEN", "test-alert-token")

from app.core.config import get_settings
from app.core.database import Base, get_db
from app.main import app
from app.models.entities import RuntimeSetting

get_settings.cache_clear()


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    # SQLite cannot use native PG enums/JSONB identically; use create_all for unit tests only.
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = TestingSession()
    session.add(RuntimeSetting(key="demo_failure_mode_enabled", value="false"))
    session.commit()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def _override_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-admin-token"}


@pytest.fixture()
def recovery_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-recovery-token"}


@pytest.fixture()
def sample_request_payload() -> dict:
    return {
        "customer_name": "Jordan Lee",
        "customer_email": "jordan.lee@example.com",
        "service_category": "Technical Support",
        "title": "Printer offline",
        "description": "Warehouse printer cannot join the network.",
        "priority": "high",
    }
