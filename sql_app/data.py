from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, not_
from sqlalchemy import func
from typing import Union
import sql_app.models as models
import sql_app.schemas as schemas
from sqlalchemy.sql import text

class EmployeeMethod:
    def create_employee(db: Session, employee: schemas.EmployeeBase):
        db_employee = models.Employee(name = employee.employeeName, departmentId = employee.departmentIn)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    def get_by_id(db: Session, employeeId: int):
        return db.query(models.Employee.id.label("ID"), models.Employee.name.label("Name")).filter(models.Employee.id == employeeId).all()
    def get_rate(db: Session, employeeId: int):
        return db.query(models.Employee.id.label("ID"), models.Employee.rate.label("Rate")).filter(models.Employee.id == employeeId).all()

    def update_rate(db: Session, employee: schemas.EmployeeRate):
        db_rate_update = db.query(models.Employee).filter(
            and_(
                models.Employee.id == employee.id
            )
        ).update({
            'rate': employee.rate
        })
        db.commit()
        return db.query(models.Employee).filter(
            and_(
                models.Employee.id == employee.id
            )
        ).first()

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

    def get_project(db:Session, id: Union[str, None] = None, name: Union[str, None] = None, status: Union[str, None] = None):
        return db.query(models.Project).filter(
            or_(
                models.Project.id == id, 
                models.Project.name == name,
                models.Project.status == status,
            )
        ).all()  

    def update_project(db: Session, project: schemas.Department):
        db_project_update = db.query(models.Project).filter(
            and_(
                models.Project.id == project.projectid
            )
        ).update({
            'name': project.projectName,
            'status': project.projectStatus,
        })
        db.commit()
        return db.query(models.Project).filter(
            and_(
                models.Project.id == project.projectid
            )
        ).first()
    
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
    
    def get_employee_projectSalary(db: Session, participate: schemas.ParticipateBase):
        return db.query(models.Employee.name.label('Họ tên'),
                        models.Project.name.label('Dự án'),
                        models.Participate.finalSalary.label('Lương tháng')).join(models.Employee).join(models.Project).filter(
            and_(
                models.Participate.employeeId == participate.employeeId,
                models.Participate.projectId == participate.projectId
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

    def get_avgFinalSalary_department(db: Session, departmentid: int):
        return db.query(models.Employee.departmentId,
                        func.avg(models.Participate.finalSalary).label('Lương tháng trung bình')
                        ).select_from(models.Employee).join(models.Participate).filter(
                            and_(models.Employee.id == models.Participate.employeeId)
                        ).group_by(models.Employee.departmentId).having(models.Employee.departmentId == departmentid).all()
    
    def get_name_department(db: Session, departmentid:int):
        return db.query(models.Department.name.label('Phòng ban')).filter(models.Department.id == departmentid).all()

    def get_list(db: Session):
        return db.query(models.Employee.departmentId.label('Mã phòng ban'),
                        func.avg(models.Participate.finalSalary).label('Lương tháng trung bình')
                        ).select_from(models.Employee).join(models.Participate).filter(
                            and_(models.Employee.id == models.Participate.employeeId)
                        ).group_by(models.Employee.departmentId).where(models.Employee.departmentId>0).all()
    
    def get_list_deparment_name(db: Session):
        return db.query(models.Department.name.label("Phòng ban")).all()

    def get_all(db:Session):
        return db.query(models.Project).all()

class ProjectAndEmployeeMethod:
    def get_all_employee(db: Session, employeeid: Union[int, None]):
        return db.query(models.Employee.id.label('Mã nhân viên'),
                        models.Project.id.label('Mã dự án'),
                        models.Project.name.label('Dự án'),
                        models.Participate.finalSalary.label('Tổng lương tháng')).join(models.Employee).join(models.Project).filter(models.Employee.id == employeeid).all()

    def get_project_salary(db: Session, projectid: Union[int, None]):
        return db.query(models.Employee.id.label('Mã nhân viên'),
                        models.Project.name.label('Dự án'),
                        models.Participate.finalSalary.label('Tổng lương tháng')).join(models.Employee).join(models.Project).filter(models.Project.id == projectid).all()

    def get_all_project(db:Session, status:Union[str,None]):
        return db.query(models.Project.id.label('Mã dự án'),
                        models.Project.name.label('Dự án'),
                        models.Project.status.label('Trạng thái dự án')).all()

    def get_all_project_all(db: Session):
        return db.query(models.Project.id.label('Mã dự án'),
                        models.Project.name.label('Dự án'),
                        models.Project.status.label('Trạng thái dự án')).all()

class BonusProjectMethod:
    def get_all_bonus(db: Session, projectid: Union[int, None]):
        return db.query(models.Employee.id.label('Mã nhân viên'),
                        models.Project.name.label('Dự án'),
                        models.Participate.bonus.label('Lương thưởng')).join(models.Employee).join(models.Project).filter(models.Project.id == projectid).all()

class EmployeeInformationMethod:
    def find_employee(db: Session, employeeInfor: schemas.EmployeeFind):
            return db.query(
                models.Employee.name.label('Họ và tên'),
                models.Project.name.label('Dự án'),                
                models.Participate.position.label('Chức vụ'),
                models.Participate.finalSalary.label('Tổng lương tháng'),
                models.Employee.rate.label('Đánh giá'),
                models.Participate.bonus.label('Lương thưởng'),
                models.Participate.salaryProject.label('Lương trong dự án'),
                ).select_from(models.Employee).join(models.Participate).join(models.Project).filter(
                    or_(
                        models.Employee.id == employeeInfor.employeeid,
                        models.Employee.name == employeeInfor.employeeName,
                        models.Employee.rate == employeeInfor.employeeRate,
                        models.Participate.bonus == employeeInfor.employeeBonus,
                        models.Participate.salaryProject == employeeInfor.employeeSalaryProject,
                        models.Participate.finalSalary == employeeInfor.employeeFinalSalary,
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
                        models.Participate.bonus.label('Lương thưởng'),
                        models.Participate.salaryProject.label('Lương dự án'),
                        models.Participate.finalSalary.label('Tổng lương tháng')).join(models.Employee).join(models.Project).filter(
            and_(
                models.Participate.employeeId == employeeProject.employeeid,
                models.Participate.projectId == employeeProject.projectid
            )
        ).all()

    def update_employee(db: Session, salary: schemas.ProjectEmployeeCreate):
        db_employee_update = db.query(models.Participate).filter(
            and_(
                models.Participate.employeeId == salary.employeeid,
                models.Participate.projectId == salary.projectid,
            )
        ).update({
            "salaryProject" : salary.projectSalary,
            "bonus" : salary.bonusSalary,
        })
        db.commit()
        return db.query(models.Participate).filter(
            and_(
                models.Participate.employeeId == salary.employeeid,
                models.Participate.projectId == salary.projectid,
            )
        ).first()

class FinalSalaryAndRate:
    def get_list(db: Session):
        return db.query(models.Employee.id.label('Mã nhân viên'),
                        models.Employee.name.label('Họ và Tên'),
                        models.Participate.finalSalary.label('Lương tháng'),
                        models.Employee.rate.label('Đánh giá')
                        ).filter(models.Employee.id == models.Participate.employeeId).group_by(models.Employee.id).order_by((models.Employee.rate).desc(),(models.Participate.finalSalary).desc()).all()
    
    def get_listFinalSalary(db: Session):
        return db.query(
            models.Employee.name.label('Họ và Tên'),
            models.Participate.finalSalary.label('Lương tháng'),
        ).filter(models.Employee.id == models.Participate.employeeId).group_by(models.Employee.id).order_by((models.Participate.finalSalary).desc()).all()
    

class RateMethod:
    def create_Rate(db: Session, employee: schemas.EmployeeRate):
        db_rEmployee = models.Employee( rate = employee.rate)
        db.add(db_rEmployee)
        db.commit()
        db.refresh(db_rEmployee)
        return db_rEmployee

    def get_rate(db:Session, id: Union[int, None] = None, rate: Union[int, None] = None):
        return db.query(models.Employee).filter(
            or_(
                models.Employee.id== id,
                models.Employee.rate == rate,
            )
        ).all()

    def update_Rate(db: Session, employee: schemas.EmployeeRate):
        db_rate_update = db.query(models.Employee).filter(
            and_(
                models.Employee.id == employee.id
            )
        ).update({
            'rate': employee.rate,
        })
        db.commit()
        return db.query(models.Employee).filter(
            and_(
                models.Employee.id == employee.id
            )
        ).first()
   
    def get_all(db:Session):
        return db.query(models.Employee).all()

class getEmployeeInProject:
    def getEmp(projectID:int, db:Session):
        return db.query(models.Participate.employeeId.label('Tham gia')).join(models.Project).filter(models.Participate.projectId==projectID).all()

class ProjectAndEmployeeAndRateMethod:
    def get_all_rate(db:Session, projectId:schemas.EmployeeAndProject):
        return db.query(
            models.Employee.name.label('Họ và Tên'),
            models.Project.name.label('Dự án'),
            models.Employee.rate.label("Đánh giá")
            ).select_from(models.Employee).join(models.Participate).join(models.Project).filter(
            and_(
                models.Participate.projectId==projectId.projectid)).all()
    

