from typing import List, Optional
from datetime import date
from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func
from database import get_db
from model import (
    EmployeeCreate,
    EmployeeUpdate,
    Employee,
    Department,
    DepartmentCreate,
    AttendanceCreate,
    LeaveRequestCreate,
    LeaveRequestUpdate,
)
from models_db import EmployeeDB, DepartmentDB, AttendanceDB, LeaveRequestDB


app = FastAPI(title="PK Employee Database System")

app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------- CORS --------------------


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# -------------------- HTML PAGE ROUTES --------------------


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/employees-page")
def employees_page():
    return FileResponse("static/employees.html")


@app.get("/add-employee")
def add_employee_page():
    return FileResponse("static/add_employee.html")


@app.get("/edit-employee")
def edit_employee_page():
    return FileResponse("static/edit_employee.html")


@app.get("/employee-details")
def employee_details_page():
    return FileResponse("static/employee_details.html")


@app.get("/department-report")
def department_report_page():
    return FileResponse("static/department_report.html")


@app.get("/attendance")
def attendance_page():
    return FileResponse("static/attendance.html")


@app.get("/leaves")
def leaves_page():
    return FileResponse("static/leaves.html")


@app.get("/departments")
def departments_page():
    return FileResponse("static/departments.html")


# -------------------- EMPLOYEE ENDPOINTS --------------------


@app.get("/api/employees", response_model=List[Employee])
def get_all_employees(db: Session = Depends(get_db)):
    rows = (
        db.query(EmployeeDB, DepartmentDB.name.label("department_name"))
        .outerjoin(DepartmentDB, EmployeeDB.department_id == DepartmentDB.id)
        .order_by(EmployeeDB.id)
        .all()
    )

    result = []
    for emp, department_name in rows:
        result.append(
            Employee(
                id=emp.id,
                full_name=emp.full_name,
                email=emp.email,
                phone=emp.phone,
                position=emp.position,
                department_id=emp.department_id,
                salary=float(emp.salary),
                hire_date=emp.hire_date,
                status=emp.status,
                department_name=department_name,
            )
        )
    return result


@app.get("/api/employees/{emp_id}", response_model=Employee)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(EmployeeDB, DepartmentDB.name.label("department_name"))
        .outerjoin(DepartmentDB, EmployeeDB.department_id == DepartmentDB.id)
        .filter(EmployeeDB.id == emp_id)
        .first()
    )

    if not row:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp, department_name = row
    return Employee(
        id=emp.id,
        full_name=emp.full_name,
        email=emp.email,
        phone=emp.phone,
        position=emp.position,
        department_id=emp.department_id,
        salary=float(emp.salary),
        hire_date=emp.hire_date,
        status=emp.status,
        department_name=department_name,
    )


@app.post("/api/employees", status_code=status.HTTP_201_CREATED)
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    existing_email = db.query(EmployeeDB).filter(EmployeeDB.email == emp.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    department = db.query(DepartmentDB).filter(DepartmentDB.id == emp.department_id).first()
    if not department:
        raise HTTPException(status_code=400, detail="Invalid department_id")

    new_employee = EmployeeDB(
        full_name=emp.full_name,
        email=emp.email,
        phone=emp.phone,
        position=emp.position,
        department_id=emp.department_id,
        salary=emp.salary,
        hire_date=emp.hire_date,
        status=emp.status,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "id": new_employee.id,
        "message": "Employee created successfully"
    }


@app.put("/api/employees/{emp_id}")
def update_employee(emp_id: int, emp: EmployeeUpdate, db: Session = Depends(get_db)):
    existing_employee = db.query(EmployeeDB).filter(EmployeeDB.id == emp_id).first()
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = emp.model_dump(exclude_unset=True)

    if "email" in update_data:
        email_exists = (
            db.query(EmployeeDB)
            .filter(EmployeeDB.email == update_data["email"], EmployeeDB.id != emp_id)
            .first()
        )
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already exists")

    if "department_id" in update_data:
        department = db.query(DepartmentDB).filter(DepartmentDB.id == update_data["department_id"]).first()
        if not department:
            raise HTTPException(status_code=400, detail="Invalid department_id")

    for key, value in update_data.items():
        setattr(existing_employee, key, value)

    db.commit()
    db.refresh(existing_employee)

    return {"message": "Employee updated successfully"}


@app.delete("/api/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}



# -------------------- DEPARTMENT ENDPOINTS --------------------


@app.get("/api/departments", response_model=List[Department])
def get_departments(db: Session = Depends(get_db)):
    departments = db.query(DepartmentDB).order_by(DepartmentDB.name).all()
    return departments


@app.post("/api/departments", status_code=status.HTTP_201_CREATED)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    existing_department = db.query(DepartmentDB).filter(DepartmentDB.name == dept.name).first()
    if existing_department:
        raise HTTPException(status_code=400, detail="Department already exists")

    new_department = DepartmentDB(
        name=dept.name,
        description=dept.description,
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return {
        "id": new_department.id,
        "message": "Department created successfully"
    }



# -------------------- ATTENDANCE ENDPOINTS --------------------


@app.get("/api/attendance")
def get_attendance(
    employee_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            AttendanceDB.id,
            AttendanceDB.employee_id,
            EmployeeDB.full_name.label("employee_name"),
            AttendanceDB.date,
            AttendanceDB.check_in,
            AttendanceDB.check_out,
            AttendanceDB.status,
        )
        .join(EmployeeDB, AttendanceDB.employee_id == EmployeeDB.id)
    )

    if employee_id is not None:
        query = query.filter(AttendanceDB.employee_id == employee_id)

    if start_date is not None:
        query = query.filter(AttendanceDB.date >= start_date)

    if end_date is not None:
        query = query.filter(AttendanceDB.date <= end_date)

    rows = query.order_by(AttendanceDB.date.desc()).all()

    return [
        {
            "id": row.id,
            "employee_id": row.employee_id,
            "employee_name": row.employee_name,
            "date": row.date,
            "check_in": str(row.check_in) if row.check_in else None,
            "check_out": str(row.check_out) if row.check_out else None,
            "status": row.status,
        }
        for row in rows
    ]


@app.post("/api/attendance", status_code=status.HTTP_201_CREATED)
def mark_attendance(att: AttendanceCreate, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.id == att.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing_attendance = (
        db.query(AttendanceDB)
        .filter(
            AttendanceDB.employee_id == att.employee_id,
            AttendanceDB.date == att.date,
        )
        .first()
    )

    if existing_attendance:
        existing_attendance.check_in = att.check_in
        existing_attendance.check_out = att.check_out
        existing_attendance.status = att.status
        db.commit()
        db.refresh(existing_attendance)
        return {"message": "Attendance updated successfully"}

    new_attendance = AttendanceDB(
        employee_id=att.employee_id,
        date=att.date,
        check_in=att.check_in,
        check_out=att.check_out,
        status=att.status,
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return {
        "id": new_attendance.id,
        "message": "Attendance recorded successfully"
    }


# -------------------- LEAVE REQUEST ENDPOINTS --------------------


@app.get("/api/leave-requests")
def get_leave_requests(
    employee_id: Optional[int] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            LeaveRequestDB.id,
            LeaveRequestDB.employee_id,
            EmployeeDB.full_name.label("employee_name"),
            LeaveRequestDB.start_date,
            LeaveRequestDB.end_date,
            LeaveRequestDB.reason,
            LeaveRequestDB.status,
        )
        .join(EmployeeDB, LeaveRequestDB.employee_id == EmployeeDB.id)
    )

    if employee_id is not None:
        query = query.filter(LeaveRequestDB.employee_id == employee_id)

    if status_filter is not None:
        query = query.filter(LeaveRequestDB.status == status_filter)

    rows = query.order_by(LeaveRequestDB.start_date.desc()).all()

    return [
        {
            "id": row.id,
            "employee_id": row.employee_id,
            "employee_name": row.employee_name,
            "start_date": row.start_date,
            "end_date": row.end_date,
            "reason": row.reason,
            "status": row.status,
        }
        for row in rows
    ]


@app.post("/api/leave-requests", status_code=status.HTTP_201_CREATED)
def create_leave_request(leave: LeaveRequestCreate, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.id == leave.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_leave = LeaveRequestDB(
        employee_id=leave.employee_id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="Pending",
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return {
        "id": new_leave.id,
        "message": "Leave request submitted successfully"
    }


@app.put("/api/leave-requests/{leave_id}")
def update_leave_status(leave_id: int, update: LeaveRequestUpdate, db: Session = Depends(get_db)):
    leave_request = db.query(LeaveRequestDB).filter(LeaveRequestDB.id == leave_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    leave_request.status = update.status
    db.commit()
    db.refresh(leave_request)

    return {"message": f"Leave request {update.status.lower()} successfully"}



# -------------------- DEPARTMENT REPORT / STATS --------------------


@app.get("/api/department/stats")
def department_stats(db: Session = Depends(get_db)):
    rows = (
        db.query(
            DepartmentDB.id.label("department_id"),
            DepartmentDB.name.label("department_name"),
            func.count(EmployeeDB.id).label("employee_count"),
            func.coalesce(func.sum(EmployeeDB.salary), 0).label("total_salary"),
        )
        .outerjoin(EmployeeDB, EmployeeDB.department_id == DepartmentDB.id)
        .group_by(DepartmentDB.id, DepartmentDB.name)
        .order_by(DepartmentDB.name)
        .all()
    )

    return [
        {
            "department_id": row.department_id,
            "department_name": row.department_name,
            "employee_count": row.employee_count,
            "total_salary": float(row.total_salary),
        }
        for row in rows
    ]