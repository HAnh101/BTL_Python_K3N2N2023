from typing import Union
from pydantic import BaseModel

class EmployeeBase(BaseModel):
    employeeName: str
    departmentId: int
    employeeSalary: int
    employeeRate: int

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeDepartment(EmployeeBase):
    id: int
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    projectName: str
    projectStatus: str
    
class ProjectCreate(ProjectBase):
    pass

class JoinBase(BaseModel):
    employeeId: int
    projectId: int
    joinPosition: str
    joinSalaryProject: int

class JoinCreate(JoinBase):
    pass

class EmployeeJoin(JoinBase):
    id: int
    class Config:
        orm_mode = True

class EmployeeJoinProject(JoinBase):
    id: int
    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    departmentName: str

class DepartmentCreate(DepartmentBase):
    pass
