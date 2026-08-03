"""
Central app configuration.

All secrets (Google Books API key, JWT signing secret) live here,
loaded from environment variables / a local .env file - never from
the frontend. Copy .env.example to .env and fill in real values
before running the server.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Google Books ---
    google_books_api_key: str = ""

    # --- Auth / JWT ---
    jwt_secret_key: str = "change-this-in-your-.env-file"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # --- Database ---
    database_url: str = "sqlite:///./book_finder.db"

    # --- CORS ---
    # Comma-separated list of allowed origins for the frontend.
    cors_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
