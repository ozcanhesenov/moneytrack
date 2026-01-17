from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

# SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # SQLite üçün lazımdır
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class - bütün modellər bundan inherit edəcək
Base = declarative_base()


def get_db():
    """
    Database session dependency
    FastAPI dependency injection üçün
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()