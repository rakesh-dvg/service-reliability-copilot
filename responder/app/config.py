from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "src-responder"
    alert_webhook_token: str = "dev-alert-webhook-token-change-me"
    recovery_api_token: str = "dev-recovery-token-change-me"
    backend_base_url: str = "http://backend:8000"
    remediation_cooldown_seconds: int = 120
    max_remediation_attempts: int = 2
    verification_timeout_seconds: int = 15
    groq_api_key: str | None = None
    groq_model: str = "llama-3.1-8b-instant"
    groq_enabled: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
