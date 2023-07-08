import sqlite3
import numpy as np 
import random
import string

def initDef():
    connect = sqlite3.connect('LuongNhanVien.db')
    c = connect.cursor()

    department = 8
    employeeEachDepartment = 20
    employeeSum = int(department * employeeEachDepartment)

    employeeId = np.random.randint(1, high=employeeSum)
    c.execute('''INSERT INTO "employee"("id") VALUES (?)''', employeeId)
    departmentId = np.random.randint(1, high=department)

    def setEmployeeToDepartment(departmentId):
        firstName = firstNameList[int(np.floor(len(firstNameList) * np.random.random()))]
        middleName =  middleNameList[int(np.floor(len(middleNameList) * np.random.random()))]
        lastName = random.choices(string.ascii_uppercase, k=1)
        c.execute('''INSERT INTO "employee"("name", "departmentId") VALUES (?, ?)''', [f'{firstName} {middleName} {lastName[0]}', departmentId])

    def departmentIsReady(departmentId, employeeEachDepartment, department):
    employeeInDepartment = c.execute('''SELECT * FROM "employee" WHERE departmentId == ?''', [departmentId])
    
    if(len(employeeInDepartment.fetchall()) < employeeEachDepartment):
        return departmentId

    middleNameList = ["Hoàng", "Văn", "Quang", "Quốc", "Thị", "Minh"]
    firstNameList = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương" ,"Lý"]

    salary = 10000
    c.execute('''INSERT INTO "employee"("salary") VALUES (10000)''', salary)
    rate = np.random.randint(1, high=5)
    c.execute('''INSERT INTO "employee"("rate") VALUES (?)''', rate)

    project = 30
    projectId = np.random.randint(1, hight=project)
    c.execute('''INSERT INTO "project"("id") VALUES (?)''', projectId)
    
    statusList = ["Đạt", "Không đạt"]
    status = random.choice(statusList)
    c.execute('''INSERT INTO "project"("status") VALUES (?)''', status)
    
    positionList = ["Trưởng nhóm", "Thành viên"]
    position = random.choice(positionList)
    c.execute('''INSERT INTO "join"("position") VALUES (?)''', position)

    salaryProject = 2000
    c.execute('''INSERT INTO "join"("salaryProject") VALUES (2000)''', salaryProject)

    listDepartment = [
        ["Phòng kế toán"],
        ["Phòng kiểm toán"],
        ["Phòng nhân sự"],
        ["Phòng hành chính"],
        ["Phòng chăm sóc khách hàng"],
        ["Phòng công nghệ thông tin"],
        ["Phòng marketing"],
        ["Phòng kinh doanh"],
    ]
    c.executemany('''INSERT INTO "department"("name") VALUES (?)''', listDepartment)
 
    connect.commit()
    connect.close()