# 🚀 PK Employee Database System

A full-stack **Employee Management System** built using **FastAPI**, **PostgreSQL**, and modern web technologies.

This system helps manage employees, departments, attendance, and leave requests efficiently with a clean UI and scalable backend.

---

## 📌 Features

- 👨‍💼 Employee Management (Add, Edit, View, Delete)  
- 🏢 Department Management  
- 📊 Attendance Tracking  
- 📝 Leave Request Management  
- 📊 Reports & Analytics  
- 💰 Salary Insights  
- ⚡ FastAPI Backend (High Performance)  
- 🗄️ PostgreSQL Database Integration  
- 🔐 Environment-based Configuration (.env)  
- 🌐 Static Frontend (HTML Pages)  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Validation:** Pydantic  
- **Server:** Uvicorn  
- **Frontend:** HTML, CSS, JavaScript  
- **Config:** python-dotenv  

---

## 📁 Project Structure
pk_employee_database_system/
│
├── static/
│ ├── images/ # UI images & assets
│ ├── add_employee.html
│ ├── employees.html
│ ├── attendance.html
│ ├── departments.html
│ └── ...
│
├── alembic/ # Database migrations
├── database.py # DB connection setup
├── main.py # FastAPI entry point
├── model.py # Pydantic schemas
├── models_db.py # SQLAlchemy models
├── requirements.txt # Dependencies
├── .env # Environment variables (ignored)
├── venv/ # Virtual environment (ignored)
└── README.md # Documentation


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/RavishankarGavhane/pk-employee-management-system.git
cd pk_employee_database_system
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Linux/Mac

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup Environment Variables

Create a .env file:

DATABASE_URL=postgresql://postgres:password@localhost:5432/pk_employee_database_system
5️⃣ Run the Application
uvicorn main:app --reload

Open in browser:

👉 http://127.0.0.1:8000

🗄️ Database Setup

Make sure PostgreSQL is installed and running.

CREATE DATABASE pk_employee_database_system;
🔌 API Endpoints
👨‍💼 Employees
GET /api/employees
POST /api/employees
PUT /api/employees/{id}
DELETE /api/employees/{id}
🏢 Departments
GET /api/departments
POST /api/departments
📊 Attendance
GET /api/attendance
POST /api/attendance
📝 Leave Requests
GET /api/leave-requests
POST /api/leave-requests
PUT /api/leave-requests/{id}
📸 Application Screenshots
🏠 Dashboard
<img src="./static/images/Dashboard.png" width="800">
👨‍💼 Employee Management
<img src="./static/images/employee_directory.png" width="800">
➕ Add New Employee
<img src="./static/images/add_new_employee.png" width="800">
🏢 Department Management
<img src="./static/images/department_management.png" width="800">
📊 Department Analytics
<img src="./static/images/department_analytics.png" width="800">
👥 Department Wise Employee Count
<img src="./static/images/department_empl_count.png" width="800"> <img src="./static/images/dep_wise_count.png" width="800"> <img src="./static/images/dept_wise_emp_count.png" width="800">
📊 Full Department Report
<img src="./static/images/dept_wise_full_report.png" width="800">
📊 Attendance Management
<img src="./static/images/attendance_management.png" width="800">
📊 Attendance Summary
<img src="./static/images/attendance_summary.png" width="800">
📝 Leave Requests
<img src="./static/images/leave_requests.png" width="800">
📈 Reports Dashboard
<img src="./static/images/report.png" width="800"> <img src="./static/images/repeortdetails.png" width="800">
💰 Salary Analytics

Total Salary & Employee Count
<img src="./static/images/total_salary_empl_count.png" width="800">

Average Salary (Company)
<img src="./static/images/avrage_salry_compny.png" width="800">

Highest Paid Employee
<img src="./static/images/highest_paid_emp.png" width="800">

👨‍💼 Employee + Department Join View
<img src="./static/images/emp_with_deprtment_name_join.png" width="800">
📊 Total Employees
<img src="./static/images/total_emp.png" width="800">
⚡ Future Improvements
🔐 JWT Authentication
👥 Role-Based Access Control
📊 Advanced Dashboard Charts
🌐 React / Next.js Frontend
☁️ Cloud Deployment (AWS / Azure / Docker)
📁 Employee Profile Image Upload
👨‍💻 Author

Ravishankar Gavhane
Sr Python Developer
📍 Pune, Maharashtra

📄 License

This project is for learning and internal use.

⭐ Support

If you like this project:

👉 Give it a ⭐ on GitHub
👉 Share it with your network