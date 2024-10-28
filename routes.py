from fastapi import APIRouter,HTTPException,status,Depends
from models import Employee
from sqlalchemy.orm import Session
from schema import CreateEmployee,UpdateEmployee
from database import get_db
from sqlalchemy import or_
import oauth2

route = APIRouter(prefix='/api/employees')

@route.post('',status_code=status.HTTP_201_CREATED)
def create_emp(employee:CreateEmployee,db:Session=Depends(get_db),admin:bool = Depends(oauth2.get_current_user)):

    check_emp = db.query(Employee).filter(Employee.email==employee.email)
    if check_emp.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='emailid already exist')
    new_employee = Employee(**dict(employee))
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee



@route.get('/')
def emp_list(department: str = '',role: str = '',page: int = 1,per_page: int = 10,db: Session = Depends(get_db),admin:bool = Depends(oauth2.get_current_user)):
    offset = (page - 1) * per_page

    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department.ilike(f"%{department}%"))
    if role:
        query = query.filter(Employee.role.ilike(f"%{role}%"))

    employees = query.offset(offset).limit(per_page).all()

    if not employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No Employees')
    return employees



@route.get('/{id}')
def emp_list(id:int,db:Session=Depends(get_db),admin:bool = Depends(oauth2.get_current_user)):
    employee = db.query(Employee).filter(Employee.id==id).first()

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Employee not exist with this id')
    
    return employee



@route.put('/{id}')
def update_employee(id: int, employee_update: UpdateEmployee, db: Session = Depends(get_db),admin:bool = Depends(oauth2.get_current_user)):
    employee = db.query(Employee).filter(Employee.id == id).first()
    
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Employee not exist with this id')
    
    update_data = {key: value for key, value in employee_update.dict().items() if value is not None}
    
    db.query(Employee).filter(Employee.id == id).update(update_data)
    db.commit()
    db.refresh(employee)
    
    return employee


