import os
from pathlib import Path

from dotenv import load_dotenv

# backend/app/config.py -> parents[2] is the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)


class Settings:
    def __init__(self) -> None:
        self.database_url: str = os.getenv("DATABASE_URL", "")
        if not self.database_url:
            raise RuntimeError(
                "DATABASE_URL is not set. Copy .env.example to .env in the project root "
                "and set DATABASE_URL."
            )
        origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
        self.cors_origins: list[str] = [o.strip() for o in origins.split(",") if o.strip()]


settings = Settings()
