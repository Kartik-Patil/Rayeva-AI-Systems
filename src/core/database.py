"""
Database configuration and session management for Rayeva AI Systems.
Uses SQLAlchemy with async support.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .config import settings


# Create declarative base for models
Base = declarative_base()

# Database engine
if settings.database_url.startswith("sqlite"):
    # SQLite async engine
    async_database_url = settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    engine = create_async_engine(
        async_database_url,
        echo=settings.debug,
        future=True
    )
else:
    # PostgreSQL async engine
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        future=True,
        pool_size=10,
        max_overflow=20
    )

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session with automatic cleanup.
    
    Usage:
        async with get_db_session() as session:
            result = await session.execute(query)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_database():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[DB] Database initialized successfully")


async def drop_database():
    """Drop all database tables (use with caution)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("[DB] Database dropped")
