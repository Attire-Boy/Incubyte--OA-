"""Database engine and session management (SQLAlchemy 2.x)."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Declarative base class shared by all ORM models."""


class Database:
    """Owns the engine and session factory for one database URL."""

    def __init__(self, url: str) -> None:
        connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
        self.engine = create_engine(url, connect_args=connect_args)
        self.session_factory = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)

    def create_all(self) -> None:
        # Import models so they register with Base.metadata before creating tables.
        from app import models  # noqa: F401

        Base.metadata.create_all(self.engine)

    def new_session(self) -> Session:
        return self.session_factory()

    def dispose(self) -> None:
        self.engine.dispose()
