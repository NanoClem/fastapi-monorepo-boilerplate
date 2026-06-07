from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import db_manager


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db_manager.get_session() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db)]
