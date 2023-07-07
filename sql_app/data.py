from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, not_
from sqlalchemy import func
from typing import Union
import sql_app.models as models
import sql_app.schemas as schemas

class EmployeeMethod:
    def create_employee(db: Session, employee: schemas.EmployeeCreate):
        db_employee = models.Employee(name = employee.employeeName, departmentId = department.departmentId, salary = employee. employeeSalary, rate = employee.employeeRate)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    
    def get_employee(db:Session, id: int, name: str, departmentId: int, salary: int, rate: int):
        return db.query(models.Employee).filter(
            or_(
                models.Employee.id == id, 
                models.Employee.name == name, 
                models.Department.id == departmentId, 
                models.Employee.salary == salary,
                models.Employee.rate == rate,   
            )
        ).all()
    
    def get_all(db:Session):
        return db.query(models.Employee).all()

class ProjectMethod:
    def create_project(db: Session, project : schemas.ProjectCreate):
        db_project = models.Subject(name = project.projectName, status = project.projectStatus)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    def get_all(db:Session):
        return db.query(models.Project).all()
    
    def get_project(db:Session, id: int, name: str):
        return db.query(models.Project).filter(
            or_(
                models.Project.id == id, 
                models.Project.name == name,
            )
        ).all()
    
class JoinMethod:
    def create_join(db: Session, join: schemas.JoinCreate):
        db_join = models.Join(employeeId = employee.employeeId, projectId = project.projectId, position = join.position, salaryProject = join.joinSalaryProject)
        db.add(db_join)
        db.commit()
        db.refresh(db_join)
        return db_join

    def get_all(db:Session):
        return db.query(models.Join).all()
    
    def get_join(db:Session, employeeId: int, projectId: int, position: str, salaryProject: int):
        return db.query(models.Join).filter(
            or_(
                models.Employee.id == employeeId, 
                models.Project.id == projectId,
                models.Join.position == position, 
                models.Join.salaryProject == salaryProject,
            )
        ).all()

class DepartmentMethod:
    def create_department(db: Session, department: schemas.DepartmentCreate):
        db_department = models.Department(name = department.departmentName)
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department

    def get_all(db:Session):
        return db.query(models.Department).all()
    
    def get_department(db:Session, id: int, name: str):
        return db.query(models.Department).filter(
            or_(
                models.Department.id == id, 
                models.Department.name == name,
            )
        ).all()
