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
    def get_by_id(db: Session, employeeId: int):
        return db.query(models.Employee.id.label("ID"), models.Employee.name.label("Name")).filter(models.Employee.id == employeeId).all()

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

    def get_project_name(db:Session, name: str):
        return db.query(models.Project).filter(models.Project.name == name).all()
    
class ParticipateMethod:
    def create_participate(db: Session, participate: schemas.ParticipateCreate):
        db_participate = models.Participate(
            employeeId = participate.employeeId,
            projectId = participate.projectId,
            position = participate.position,
            salaryProject = participate.salaryProject,
            bonus = participate.bonus,
            finalSalary = participate.finalSalary,
            )
        db.add(db_participate)
        db.commit()
        db.refresh(db_participate)
        return db_participate
    
    def get_participate(db:Session, employeeId: int, projectId: int, position: str, salaryProject: int, bonus: int, finalSalary: int):
        return db.query(models.Participate).filter(
            or_(
                models.Employee.id == employeeId, 
                models.Project.id == projectId,
                models.Participate.position == position, 
                models.Participate.salaryProject == salaryProject,
                models.Participate.bonus == bonus,
                models.Participate.finalSalary == finalSalary,
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
                        models.Project.name.label('Dự án'),
                        models.Participate.finalSalary.label('Tổng lương tháng')).join(models.Employee).join(models.Project).filter(models.Employee.id == employeeid).all()

class BonusProjectMethod:
    def get_all_bonus(db: Session, projectid: Union[int, None]):
        return db.query(models.Employee.id.label('Mã nhân viên'),
                        models.Project.name.label('Dự án'),
                        models.Participate.bonus.label('Lương thưởng')).join(models.Employee).join(models.Project).filter(models.Project.id == projectid).all()

class EmployeeInformationMethod:
    def find_employee(db: Session, employeeInfor: schemas.EmployeeFind):
            return db.query(
                models.Employee.name.label('Họ và tên'),
                models.Department.name.label('Phòng ban'),
                models.Project.name.label('Dự án'),                
                models.Participate.finalSalary.label('Tổng lương tháng'),
                models.Employee.rate.label('Đánh giá'),
                models.Participate.bonus.label('Lương thưởng'),
                models.Participate.position.label('Chức vụ'),
                models.Participate.salaryProject.label('Lương trong dự án'),
                ).select_from(models.Employee).join(models.Department).join(models.Participate).join(models.Project).filter(
                    or_(
                        models.Employee.id == employeeInfor.employeeid,
                        models.Employee.name == employeeInfor.employeeName,
                        models.Department.name == employeeInfor.departmentName,
                        models.Project.name == employeeInfor.projectName,
                        models.Participate.finalSalary == employeeInfor.employeeFinalSalary,
                        models.Employee.rate == employeeInfor.employeeRate,
                        models.Participate.bonus == employeeInfor.employeeBonus,
                        models.Participate.position == employeeInfor.employeePosition,
                        models.Participate.salaryProject == employeeInfor.employeeSalaryProject,
                    )
                ).all()

class SalaryProjectSumMethod:
    def get_all_employee(db: Session, employeeid: Union[int, None]):
        return db.query(models.Employee.id.label('Mã nhân viên'),
                        models.Project.name.label('Dự án'),
                        models.Participate.salaryProject.label('Tổng lương trong dự án')).join(models.Employee).join(models.Project).filter(models.Employee.id == employeeid).all()

class ProjectEmployeeMethod:
    def get_employee(db: Session, employeeProject: schemas.ProjectEmployeeBase):
        return db.query(models.Employee.name.label('Họ và tên'),
                        models.Project.name.label('Dự án'),
                        models.Participate.finalSalary.label('Tổng lương')).join(models.Employee).join(models.Project).filter(
            and_(
                models.Participate.employeeId == employeeProject.studentid,
                models.Participate.projectId == employeeProject.projectid
            )
        ).all()