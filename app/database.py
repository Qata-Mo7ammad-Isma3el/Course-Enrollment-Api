import os
from typing import Generator

from pydantic_settings import BaseSettings
from sqlmodel import Session, SQLModel, create_engine

# --- 1. Define Settings (Configuration) ---
# pydantic_settings handles loading from .env automatically
class Settings(BaseSettings):
    """
    Settings class to load environment variables.
    pydantic-settings looks for variables in the environment
    and then in a .env file (if available).
    """
    database_url: str = os.getenv("DATABASE_URL")
    
    # Nested class to configure where to find the .env file
    class Config:
        env_file = ".env"

# Instantiate settings to load configuration
settings = Settings()

# --- 2. Create Engine ---
# The echo=True option is useful for debugging as it logs all SQL queries
# sent to the database. Set to False in production.
engine = create_engine(settings.database_url, echo=True)

# --- 3. Table Creation ---
def create_db_and_tables():
    """
    Creates all tables defined in SQLModel metadata (from app/models.py).
    It should be called at application startup.
    """
    # This automatically uses the SQLModel classes defined in models.py
    # because they inherit from SQLModel.
    SQLModel.metadata.create_all(engine)

# --- 4. Session Dependency (For FastAPI) ---
def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency function to provide a database session.
    It yields the session and ensures it is closed after the request.
    """
    with Session(engine) as session:
        print("#!!!!! Database session created")
        yield session
        print("#!!!!! Database session closed")