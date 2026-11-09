from sqlalchemy.orm import Session

from app.models.entities import RuntimeSetting

DEMO_FAILURE_KEY = "demo_failure_mode_enabled"


def get_setting(db: Session, key: str, default: str = "false") -> str:
    row = db.get(RuntimeSetting, key)
    if row is None:
        return default
    return row.value


def set_setting(db: Session, key: str, value: str) -> RuntimeSetting:
    row = db.get(RuntimeSetting, key)
    if row is None:
        row = RuntimeSetting(key=key, value=value)
        db.add(row)
    else:
        row.value = value
    db.flush()
    return row


def is_demo_failure_enabled(db: Session) -> bool:
    return get_setting(db, DEMO_FAILURE_KEY, "false").lower() == "true"


def set_demo_failure(db: Session, enabled: bool) -> None:
    set_setting(db, DEMO_FAILURE_KEY, "true" if enabled else "false")
