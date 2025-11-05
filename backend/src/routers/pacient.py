from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Doctor(BaseModel):
    ...

@router.put(
    "/api/appointments",
    status_code=201,
    description="Создать приём к доктору"
)
async def get_doctors():
    ...