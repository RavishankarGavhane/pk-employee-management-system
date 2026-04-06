from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, time
from typing import Optional


class EmployeeBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    position: str
    department_id: int
    salary: float
    hire_date: date
    status: Optional[str] = "Active"


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    department_id: Optional[int] = None
    salary: Optional[float] = None
    hire_date: Optional[date] = None
    status: Optional[str] = None


class Employee(EmployeeBase):
    id: int
    department_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: str = "Present"


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    id: int
    employee_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class LeaveRequestBase(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: str
    status: str = "Pending"


class LeaveRequestCreate(LeaveRequestBase):
    pass


class LeaveRequestUpdate(BaseModel):
    status: str


class LeaveRequest(LeaveRequestBase):
    id: int
    employee_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)