from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Header
from sqlalchemy import select
from database.models import UsersModel
from dependencies import Session, User, get_current_user
from enum import IntEnum
import os

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRole(IntEnum):
    DOCTOR = 0
    ADMIN = 1

def create_access_token(user_data) -> str:
    to_encode = user_data.copy()
    expire_data = datetime.now() + timedelta(minutes=15)
    to_encode.update({'exp': expire_data})
    token = jwt.encode(to_encode, os.getenv('AUTH_SECRET_KEY'))
    return token

def verify_password(password, hashed_password):
    return ctx.verify(password, hashed_password)


async def get_user_by_username(session: Session, username: str):
    result = await session.execute(
        select(UsersModel)
        .where(UsersModel.username == username)
    )
    
    return result.scalar_one_or_none()

async def get_current_user(
    session: Session,
    authorization: str = Header()
):
    try:
        payload = jwt.decode(
            authorization,
            os.getenv('AUTH_SECRET_KEY'),
            ["HS256"]
        )
        username: str = payload.get("username")
        if not username:
            raise 
        
    except JWTError:
        raise 
    
    user = await get_user_by_username(session, username)
    if not user:
        raise
    
    return user

def requires_role(roles: list[UserRole]):
    roles = [
        role.value 
        if isinstance(role, UserRole) 
        else role 
        for role in roles
    ]
    
    async def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=404)
        return current_user
    return role_checker