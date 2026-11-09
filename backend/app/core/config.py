from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "service-reliability-copilot-backend"
    environment: str = "local"
    demo_mode: bool = True
    database_url: str = "postgresql+psycopg://src_user:src_pass@localhost:5432/src_db"
    admin_api_token: str = "dev-admin-token-change-me"
    recovery_api_token: str = "dev-recovery-token-change-me"
    alert_webhook_token: str = "dev-alert-webhook-token-change-me"
    cors_origins: str = "http://localhost:5173,http://localhost:3000,http://localhost"
    otel_exporter_otlp_endpoint: str = "http://localhost:4318"
    otel_service_name: str = "src-backend"
    enable_otel: bool = True
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
