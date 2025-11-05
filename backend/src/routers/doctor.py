from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from src.dependencies import Session

from src.database.models import (
    EmployeesModel, 
    EmployeeHiringFormatsModel, 
    EmployeePositionsModel,
    HospitalsModel
)

router = APIRouter()

class Hospital(BaseModel):
    name: str
    street: str

class Doctor(BaseModel):
    id: int
    last_name: str
    first_name: str
    patronymic: str
    position: str
    hiring_format: str
    hospital: Hospital
    
@router.get(
    "/api/doctors",
    status_code=200, response_model=List[Doctor],
    description="Получить всех докторов"
)
async def get_doctors(
    session: Session
):
    result = await session.execute(
        select(
            EmployeesModel.id,
            EmployeesModel.last_name,
            EmployeesModel.patronymic,
            EmployeePositionsModel.title.label('position'),
            EmployeeHiringFormatsModel.name.label('hiring_format'),
            HospitalsModel.name.label('hospital_name'),
            HospitalsModel.street.label('hospital_street')
        )
        .join(
            EmployeePositionsModel, 
            EmployeePositionsModel.id == EmployeesModel.position_id
        )
        .join(
            EmployeeHiringFormatsModel, 
            EmployeeHiringFormatsModel.id == EmployeesModel.hiring_format_id
        )
        .join(
            HospitalsModel, 
            HospitalsModel.id == EmployeesModel.hospital_id
        )
    )
    
    return [
        Doctor(
            id=doctor.id,
            last_name=doctor.last_name,
            first_name=doctor.first_name,
            patronymic=doctor.patronymic,
            position=doctor.position,
            hiring_format=doctor.hiring_format,
            hospital=Hospital(
                name=doctor.hospital_name,
                street=doctor.hospital_street
            )
            
        )
        for doctor in result.all()
    ]
    
@router.put(
    "/api/doctors",
    status_code=201,
    description="Зарегистрировать нового доктора"
)
async def add_doctor(
     session: Session, new_doctor: Doctor
):
    ...