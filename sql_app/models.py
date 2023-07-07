from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(20), nullable=False)
    departmentId = Column(Integer, ForeignKey("department.id"), nullable=False)
    salary = Column(Integer, index=True, nullable=False)
    rate = Column(Integer, index=True, nullable=False)
    
    departmentIn = relationship("Department", back_populates="employees")
    joinIn = relationship("Join", back_populates="employeeJoin")
    
class Project(Base):
    __tablename__ = "project"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    status = Column(String(10), nullable=False)

    projectJoin = relationship("Join", back_populates="projects")
    
class Join(Base):
    __tablename__ = "join"
    employeeId= Column(Integer, ForeignKey("employee.id"), nullable=False)
    projectId= Column(Integer, ForeignKey("project.id"), nullable=False)
    position = Column(String(20), index=True, nullable=False)
    salaryProject = Column(Integer, index=True, nullable=False)
    
    employeeJoin = relationship("Employee", back_populates="joinIn")
    projects = relationship("Project", back_populates="projectJoin")

class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)

    employees = relationship("Employee", back_populates="departmentIn")
