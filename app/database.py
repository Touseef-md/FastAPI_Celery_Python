from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


engine = create_engine(
    settings.DATABASE_URL, connect_args=settings.DATABASE_CONNECT_DICT
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get the database session
def get_db():
    """
    This function provides a context manager for database sessions.

    The function creates a new database session using the `SessionLocal` object,
    which is a configured SQLAlchemy sessionmaker bound to the application's database engine.
    The session is then yielded to the caller, allowing them to interact with the database.
    Once the caller is done with the session, it is automatically closed within the `finally` block.

    Parameters:
    None

    Returns:
    A context manager yielding a SQLAlchemy session object for database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()