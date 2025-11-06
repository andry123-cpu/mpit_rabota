from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dependencies import Session
from sqlalchemy import select
from database.models import UsersModel
from auth import (
    get_user_by_username,
    verify_password, 
    create_access_token
)


router = APIRouter()

class Token(BaseModel):
    token: str
    
class UserAuth(BaseModel):
    username: str
    password: str

@router.post(
    "/api/auth/login",
    response_model=Token,
    description="Получение токена доступа для входа в систему"
)
async def get_access_token(
    session: Session, data: UserAuth
):
    user = await get_user_by_username(session, data.username)
    if not user:
        raise HTTPException(status_code=404)
    
    print(data.password, user.password)
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401)
    
    return Token(token=create_access_token({'username': user.username}))
    