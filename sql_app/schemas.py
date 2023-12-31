from typing import Union
from pydantic import BaseModel

class EmployeeBase(BaseModel):
    employeeName: str
    departmentId: int

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    projectName: str
    projectStatus: str

class ProjectCreate(ProjectBase):
    pass

class Project(BaseModel):
    projectid: int
    projectName: str
    projectStatus: str

class ParticipateBase(BaseModel):
    employeeId: int
    projectId: int

class ParticipateCreate(ParticipateBase):
    position: str
    salaryProject: int
    bonus: int
    finalSalary: int
    class Config:
        orm_mode = True

class EmployeeParticipate(ParticipateBase):
    id: int
    class Config:
        orm_mode = True

class ParticipateProject(ParticipateBase):
    id: int
    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    departmentName: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentEmployee(DepartmentBase):
    id: int
    class Config:
        orm_mode = True

class Department(BaseModel):
    departmentName: str
    departmentid: int

class EmployeeAndProject(BaseModel):
    projectid: int
    class Config:
        orm_mode = True

class ParticipateSalary(BaseModel):
    employeeId : int
    projectId: int
    position: str
    salaryProject: int
    bonus: int

class EmployeeSalary(EmployeeBase):
    salary: int
    class Config:
        orm_mode = True

class ProjectSalary(ProjectBase):
    projectId: int
    class Config:
        orm_mode = True

class EmployeeRate(BaseModel):
    id: int
    rate: int
class avgSalaryDepartment(BaseModel):
    id: int

class EmployeeFind(BaseModel):
    employeeid: Union[int, None] = None
    employeeName: Union[str, None] = None
    employeeRate: Union[int, None] = None
    employeeBonus: Union[int, None] = None
    employeeSalaryProject: Union[int, None] = None
    employeeFinalSalary: Union[int, None] = None

class ProjectEmployeeBase(BaseModel):
    employeeid : int
    projectid: int
    class Config:
        orm_mode = True

class ProjectEmployeeCreate(BaseModel):
    employeeid : int
    projectid: int
    projectSalary: int
    bonusSalary: int
    class Config:
        orm_mode = True

class ProjectSalaryUpdate(ProjectEmployeeBase):
    projectSalary: int
    bonusSalary: int

class EmployeeBonus(BaseModel):
    employeeid: int
    projectid: int

class sum2Project(BaseModel):
    employeeid: int
    project1: int
    project2: int

class ProjectID(BaseModel):
    projectID: int

