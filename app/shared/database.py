import logging
from collections.abc import Generator
from contextlib import contextmanager
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)


def _build_database_url() -> str:
    user = environ.get("POSTGRES_USER")
    if not user:
        raise ValueError("POSTGRES_USER environment variable is not set")
    password = environ.get("POSTGRES_PASSWORD")
    if not password:
        raise ValueError("POSTGRES_PASSWORD environment variable is not set")
    db = environ.get("POSTGRES_DB")
    if not db:
        raise ValueError("POSTGRES_DB environment variable is not set")
    host = environ.get("POSTGRES_HOST", "localhost")
    port = environ.get("POSTGRES_PORT", "5432")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


# Built once at import time: the `Engine` owns its own connection pool, so a
# single module-level instance is reused for the process lifetime instead of
# spinning up a new pool (and new connections) on every call.
engine = create_engine(
    _build_database_url(),
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Borrow a `Session` from the pool and always return it.

    Commits on success, rolls back on error, and closes the session in
    a `finally` block so the underlying connection is released back to
    the pool instead of being held open or leaked.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency, e.g. `db: Session = Depends(get_db)`.

    Yields one session per request/injection and guarantees it is
    closed afterwards, so a request can never leak a pooled connection.
    """
    with session_scope() as session:
        yield session
