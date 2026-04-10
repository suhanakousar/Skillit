from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "TechPath"
    environment: str = "development"
    api_prefix: str = "/api"

    database_url: str = "postgresql+asyncpg://techpath:techpath@localhost:5432/techpath"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 60
    refresh_token_ttl_days: int = 14

    judge0_url: str = "http://localhost:2358"
    judge0_api_key: str | None = None
    use_local_runner_fallback: bool = True

    anthropic_api_key: str | None = None
    claude_model: str = "claude-sonnet-4-20250514"

    auto_bootstrap: bool = True
    seed_demo_user: bool = True
    demo_email: str = "demo@techpath.dev"
    demo_password: str = "techpath123"

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
