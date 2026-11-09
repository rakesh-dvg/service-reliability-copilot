"""Idempotent demo seed data."""

import uuid

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.entities import (
    Priority,
    RequestStatus,
    ServiceCategory,
    ServiceRequest,
)
from app.services.settings_service import set_setting


def seed() -> None:
    db = SessionLocal()
    try:
        set_setting(db, "demo_failure_mode_enabled", "false")
        existing = db.scalar(
            select(ServiceRequest).where(ServiceRequest.title == "Demo HVAC Inspection")
        )
        if existing is None:
            db.add(
                ServiceRequest(
                    id=uuid.uuid4(),
                    customer_name="Demo Customer",
                    customer_email="demo.customer@example.com",
                    service_category=ServiceCategory.GENERAL_SERVICE,
                    title="Demo HVAC Inspection",
                    description="Seeded demo request for local walkthroughs.",
                    priority=Priority.MEDIUM,
                    status=RequestStatus.OPEN,
                )
            )
        db.commit()
        print("seed_complete")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
