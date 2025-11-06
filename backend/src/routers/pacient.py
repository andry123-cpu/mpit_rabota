from datetime import datetime
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import insert

from database.models import AppointmentRequestsModel
from dependencies import Session

router = APIRouter()

class AppointmentRequest(BaseModel):
    last_name: str
    first_name: str
    patronymic: str
    age: int
    street: str | None
    apartment: int | None
    entrance: int | None
    floor: int | None
    doctor_id: int
    priority: int
    appointment_date: datetime
    
@router.post(
    "/api/appointments",
    status_code=201,
    description="Создать приём к доктору"
)
async def add_appointment_request(
    session: Session, 
    appointment: AppointmentRequest
):
    try:
        await session.execute(
            insert(AppointmentRequestsModel).values(
                last_name=appointment.last_name,
                first_name=appointment.first_name,
                age=appointment.age,
                street=appointment.street,
                apartment=appointment.street,
                entrance=appointment.entrance,
                floor=appointment.floor,
                appointment_date=appointment.appointment_date
            )
        )
        
        await session.commit()
    except Exception as e:
        await session.rollback()