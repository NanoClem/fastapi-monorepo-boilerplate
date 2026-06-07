import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import DatabaseConfig, app_config, db_config


class DatabaseManager:
    """Manages database connection and session creation."""

    def __init__(self, config: DatabaseConfig, debug: bool = False) -> None:
        self.config = config
        self.debug = debug
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    async def initialize(self) -> None:
        """Initializes the database engine and session maker."""
        self._engine = create_async_engine(
            self.config.DB_URL,
            echo=self.debug,
            pool_size=self.config.POOL_SIZE,
            pool_timeout=self.config.POOL_TIMEOUT,
            pool_recycle=self.config.POOL_RECYCLE,
            max_overflow=self.config.MAX_OVERFLOW,
            pool_pre_ping=True,  # Test connection before using it
        )

        self._session_maker = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

        # Check connection
        async with self._session_maker() as session:
            await session.execute(text("SELECT 1"))
        logging.info("Database connection verified successfully.")

    async def close(self) -> None:
        """Tears down the database engine and connection pool if initialized."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None
            logging.info("Database connection pool closed successfully")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Provides an asynchronous session for database operations."""
        if not self._session_maker:
            raise RuntimeError(
                "DatabaseManager is not initialized. Call initialize() first."
            )

        async with self._session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logging.error(f"Database transaction failed: {e}")
                await session.rollback()
                raise e
            finally:
                await session.close()


db_manager = DatabaseManager(config=db_config, debug=app_config.DEBUG)
