
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Load environment variables from day-08/.env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

# Read the PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from day-08/.env")

# Create the asynchronous database engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Create a factory for database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Provide a database session when a route needs one
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
