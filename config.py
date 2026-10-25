"""Application settings, loaded from environment variables.

Settings are an immutable value object so they can be passed explicitly into
``create_app`` (handy for tests) instead of being read from global state.
"""

import os
from dataclasses import dataclass, field

try:  # Load a local .env file when python-dotenv is installed (optional).
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip().lower() for item in value.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    database_url: str = "sqlite:///./dealership.db"
    jwt_secret: str = "change-me-in-production-please-use-a-long-random-string"
    jwt_expire_minutes: int = 60
    bcrypt_rounds: int = 12
    admin_emails: tuple[str, ...] = field(default_factory=tuple)
    cors_origins: tuple[str, ...] = ("http://localhost:5173",)

    @classmethod
    def from_env(cls) -> "Settings":
        defaults = cls()
        return cls(
            database_url=os.getenv("DATABASE_URL", defaults.database_url),
            jwt_secret=os.getenv("JWT_SECRET", defaults.jwt_secret),
            jwt_expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", defaults.jwt_expire_minutes)),
            bcrypt_rounds=int(os.getenv("BCRYPT_ROUNDS", defaults.bcrypt_rounds)),
            admin_emails=_split_csv(os.getenv("ADMIN_EMAILS", "")),
            cors_origins=_split_csv(os.getenv("CORS_ORIGINS", ",".join(defaults.cors_origins))),
        )
