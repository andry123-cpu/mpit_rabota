from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import DateTime, ForeignKey, String

from datetime import datetime

from typing import Annotated

ID = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

class Base(DeclarativeBase):
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )
    
class EmployeePositionsModel(Base):
    
    """
    Таблица для хранения специальностей врачей
    """
    
    __tablename__ = "employee_positions"
    
    id: Mapped[ID]
    title: Mapped[str] = mapped_column(String(30), nullable=False)

class EmployeeHiringFormatsModel(Base):
    
    """
    Таблица для хранения форматов приёма врачей
    """
    
    __tablename__ = "employee_hiring_formats"
    
    id: Mapped[ID]
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    
class HospitalsModel(Base):
    
    """
    Таблица для хранения медицинских учереждений
    """
    
    __tablename__ = "hospitals"
    
    id: Mapped[ID]
    name: Mapped[str] = mapped_column(String(100))
    street: Mapped[str] = mapped_column(nullable=True)

class EmployeesModel(Base):
    
    """
    Таблица для хранения врачей из разных мед. учереждений
    """
    
    __tablename__ = "employees"
    
    id: Mapped[ID]
    last_name: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    patronymic: mapped_column[str] = mapped_column(nullable=True)
    hospital_id: mapped_column[int] = mapped_column(
        ForeignKey("hospitals.id", ondelete="CASCADE")
    )
    position_id: Mapped[int] = mapped_column(
        ForeignKey("employee_positions.id", ondelete="CASCADE")
    )
    hiring_format_id: Mapped[int] = mapped_column(
        ForeignKey("employee_hiring_formats.id", ondelete="CASCADE")
    )
    
class AppointmentRequestsModel(Base):
    
    """
    Таблица для хранения заявок на приём к врачам
    """
    
    __tablename__ = "appointment_requests"
    
    id: Mapped[ID]
    
    last_name: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    patronymic: mapped_column[str] = mapped_column(nullable=True)

    age: Mapped[str] = mapped_column(nullable=False)
    
    street: Mapped[str] = mapped_column(nullable=True)
    apartment: Mapped[int] = mapped_column(nullable=True)
    entrance: Mapped[int] = mapped_column(nullable=True)
    floor: Mapped[int] = mapped_column(nullable=True)
    
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE")
    )
    
    priority: Mapped[int] = mapped_column()
    
    appointment_date: Mapped[datetime] = mapped_column(DateTime)
    
class UserRolesModel(Base):
    
    """
    Таблица для хранения ролей пользователей
    """
    
    __tablename__ = "user_roles"
    
    id: Mapped[ID]
    name: Mapped[str] = mapped_column(String(50))

class UsersModel(Base):
    
    """
    Таблица для хранения пользователей
    """
    
    __tablename__ = "users"
    
    id: Mapped[ID]
    name: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(
        ForeignKey("user_roles.id", ondelete="CASCADE")
    )
    