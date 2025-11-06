from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import insert, select
from auth import UserRole, requires_role

from dependencies import Session

from database.models import (
    EmployeesModel, 
    EmployeeHiringFormatsModel, 
    EmployeePositionsModel,
    HospitalsModel,
    UsersModel
)

router = APIRouter()

class Hospital(BaseModel):
    name: str
    street: str | None

class Doctor(BaseModel):
    id: int
    last_name: str
    first_name: str
    patronymic: str
    position: str
    hiring_format: str
    hospital: Hospital
    
class DoctorInput(BaseModel):
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
            EmployeesModel.first_name,
            EmployeesModel.patronymic,
            EmployeePositionsModel.title.label('position'),
            EmployeeHiringFormatsModel.name.label('hiring_format'),
            HospitalsModel.name.label('hospital_name'),
            HospitalsModel.street.label('hospital_street')
        )
        .join(
            EmployeePositionsModel, 
            EmployeesModel.position_id == EmployeePositionsModel.id
        )
        .join(
            EmployeeHiringFormatsModel, 
            EmployeesModel.hiring_format_id == EmployeeHiringFormatsModel.id
        )
        .join(
            HospitalsModel, 
            EmployeesModel.hospital_id == HospitalsModel.id
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
    session: Session, 
    new_doctor: DoctorInput,
    current_user: UsersModel = Depends(requires_role([UserRole.ADMIN]))
):
    await session.execute(
        insert(EmployeesModel).values(
            last_name=new_doctor.last_name,
            first_name=new_doctor.first_name,
            patronymic=new_doctor.patronymic,
            position_id=(
                select(EmployeePositionsModel.id)
                .where(
                    EmployeePositionsModel.title == new_doctor.position
                )
                .limit(1)
            ),
            hospital_id=(
                select(HospitalsModel.id)
                .where(
                    HospitalsModel.name == new_doctor.hospital.name
                )
                .limit(1)
            ),
            hiring_format_id=(
                select(EmployeeHiringFormatsModel.id)
                .where(
                    EmployeeHiringFormatsModel.name == new_doctor.hiring_format
                )
                .limit(1)
            ),
        )
    )
    
    await session.commit()
    
    return 201