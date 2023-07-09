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
    participateIn = relationship("Participate", back_populates="employeeParticipate")
    
class Project(Base):
    __tablename__ = "project"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    status = Column(String(10), nullable=False)

    projectParticipate = relationship("Participate", back_populates="projects")

class Participate(Base):
    __tablename__ = "participate"
    employeeId= Column(Integer, ForeignKey("employee.id"), primary_key=True, index=True, nullable=False)
    projectId= Column(Integer, ForeignKey("project.id"), primary_key=True, index=True, nullable=False)
    position = Column(String(20), index=True, nullable=False)
    salaryProject = Column(Integer, index=True, nullable=False)
    bonus = Column(Integer, index=True, nullable=False)
    finalSalary = Column(Integer, index=True, nullable=False)

    employeeParticipate = relationship("Employee", back_populates="participateIn")
    projects = relationship("Project", back_populates="projectParticipate")

class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)

    employees = relationship("Employee", back_populates="departmentIn")
