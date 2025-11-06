from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, Header, HTTPException
from jose import jwt, JWTError
from sqlalchemy import select
from database.models import UsersModel
from database.session import get_async_session
import os


async def get_session(request: Request):
    return request.state.db

async def db_session_middleware(request: Request, call_next):
    async with get_async_session() as session:
        request.state.db = session
        response = await call_next(request)
    return response

Session = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    session: Session,
    authorization: str = Header()
):
    try:
        payload = jwt.decode(
            authorization,
            os.getenv('AUTH_SECRET_KEY'),
            algorithms=["HS256"]
        )
        username: str = payload.get("username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(
        select(UsersModel).where(UsersModel.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

User = Annotated[UsersModel, Depends(get_current_user)]
