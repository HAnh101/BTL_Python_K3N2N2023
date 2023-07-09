from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, not_
from sqlalchemy import func
from typing import Union
import sql_app.models as models
import sql_app.schemas as schemas

class EmployeeMethod:
    def create_employee(db: Session, employee: schemas.EmployeeBase):
        db_employee = models.Employee(name = employee.employeeName, departmentId = employee.departmentIn)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    def get_byid(db: Session, employeeid: int):
        return db.query(models.Employee.id.label("ID"), models.Employee.name.label("Name")).filter(models.Employee.id == employeeid).all()

class ProjectMethod:
    def create_project(db: Session, project : schemas.ProjectBase):
        db_project = models.Project(name = project.projectName, status = project.projectStatus)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    def get_all(db:Session):
        return db.query(models.Project).all()
    
    def get_project_id(db:Session, id: int):
        return db.query(models.Project).filter(models.Project.id == id).all()
    
class JoinMethod:
    def create_join(db: Session, join: schemas.JoinCreate):
        db_join = models.Join(
            employeeId = join.employeeId,
            projectId = join.projectId,
            position = join.position,
            salaryProject = join.joinSalaryProject
            )
        db.add(db_join)
        db.commit()
        db.refresh(db_join)
        return db_join
    
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
    def create_department(db: Session, department: schemas.DepartmentBase):
        db_department = models.Department(name = department.departmentName)
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    
    def get_department(db:Session, id: Union[str, None] = None, name: Union[str, None] = None):
        return db.query(models.Department).filter(
            or_(
                models.Department.id == id, 
                models.Department.name == name,
            )
        ).all()  

    def update_department(db: Session, department: schemas.Department):
        db_department_update = db.query(models.Department).filter(
            and_(
                models.Department.id == department.departmentId
            )
        ).update({
            'name': department.departmentName,
        })
        db.commit()
        return db.query(models.Department).filter(
            and_(
                models.Department.id == department.departmentId
            )
        ).first()

    def get_all(db:Session):
        return db.query(models.Department).all()


class ProjectAndEmployeeMethod:
    def get_all_employee(db: Session, employeeid: Union[int, None]):
        return db.query(models.Employee.id.label('Mã nhân viên'),
                        models.Project.name.label('Phòng ban'),
                        models.Join.finalSalary.label('Tổng lương tháng')).join(models.Employee).join(models.Project).filter(models.Employee.id == employeeid).all()
    