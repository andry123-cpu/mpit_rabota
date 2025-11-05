from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from src.database.session import get_async_session

async def get_session():
    async with get_async_session() as session:
        yield session
        
Session = Annotated[AsyncSession, Depends(get_session)]