import json
from typing import Generator

from fastapi import Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite engine; check_same_thread=False allows usage in FastAPI async context
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator:
    """FastAPI dependency that provides a database session.

    Yields:
        Session: A SQLAlchemy session bound to the engine.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        # Ensure any exception is transformed into an HTTPException for FastAPI routes
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def init_db() -> None:
    """Create all tables defined in the SQLAlchemy models.

    This function can be called at application startup to ensure the database schema exists.
    """
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {e}")
