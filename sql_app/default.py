import sqlite3
import numpy as np 
import random
import string

def initDef():
    connect = sqlite3.connect('LuongNhanVien.db')
    c = connect.cursor()

    department = 8
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
    
    employeeEachDepartment = 20
    employeeSum = int((department * employeeEachDepartment)*0.8)
    middleNameList = ["Hoàng", "Văn", "Quang", "Quốc", "Thị", "Minh"]
    firstNameList = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương" ,"Lý"]

    # employeeId = np.random.randint(1, high=employeeSum)
    # c.execute('''INSERT INTO "employee"("id") VALUES (?)''', employeeId)
    # departmentId = np.random.randint(1, high=department)

    def departmentIsReady(departmentId, employeeEachDepartment, department):
        employeeInDepartment = c.execute('''SELECT * FROM "employee" WHERE departmentId == ?''', [departmentId])
    
        if(len(employeeInDepartment.fetchall()) < employeeEachDepartment):
            return departmentId
        else:
            departmentIdNew = int(np.ceil((department *employeeEachDepartment) * np.random.random()))
            employeeEachDepartmentNew = employeeEachDepartment
            departmentNew = department
            return departmentIsReady(departmentIdNew, employeeEachDepartmentNew, departmentNew)
        
    salary = 10000
    
    def setEmployeeToDepartment(departmentId):
        firstName = firstNameList[int(np.floor(len(firstNameList) * np.random.random()))]
        middleName =  middleNameList[int(np.floor(len(middleNameList) * np.random.random()))]
        lastName = random.choices(string.ascii_uppercase, k=1)
        # c.execute('''INSERT INTO "employee"("salary") VALUES (?)''', salary)
        rate = np.random.randint(1, high=5)
        # c.execute('''INSERT INTO "employee"("rate") VALUES (?)''', rate)
        c.execute('''INSERT INTO "employee"("name", "departmentId", "salary", "rate") VALUES (?, ?, ?, ?)''', [f'{firstName} {middleName} {lastName[0]}', departmentId, salary, rate])

    for eachEmployee in range (0, employeeSum):
        departmentId = int(np.ceil(department *(employeeEachDepartment) / np.random.random()))
        setEmployeeToDepartment(departmentIsReady(departmentId, employeeEachDepartment, department))

    listProject = [
        ["Toán"],
        ["Văn"],
        ["Tiếng Anh"],
        ["Vật lý"],
        ["Hóa học"],
        ["Sinh học"],
        ["Lịch sử"],
        ["Địa lý"],
        ["Giáo dục công dân"],
        ["Thể dục"]
    ]
    statusList = ["Đạt", "Không đạt"]
    # status = "Đạt"
    # c.execute('''INSERT INTO "project"("status") VALUES (?)''', status)
    # c.executemany('''INSERT INTO "project"("name") VALUES (?)''', listProject)
    
    def setProject(projectId):
        name = listProject[int(np.floor(len(listProject) * np.random.random()))]
        status = statusList[int(np.floor(len(statusList) * np.random.random()))]
        # c.execute('''INSERT INTO "employee"("salary") VALUES (?)''', salary)
        # c.execute('''INSERT INTO "employee"("rate") VALUES (?)''', rate)
        c.execute('''INSERT INTO "project"("name", "status") VALUES (?, ?)''', [f'{name}', status])

    for eachEmployee in range (0, employeeSum):
        projectId = np.random.randint(1, high=5)
        setProject(projectId)

    # salary = 10000
    # c.execute('''INSERT INTO "employee"("salary") VALUES (?)''', salary)
    # rate = np.random.randint(1, high=5)
    # c.execute('''INSERT INTO "employee"("rate") VALUES (?)''', rate)
    positionList = ["Trưởng nhóm", "Thành viên"]

    for employee in range(0, employeeSum):
        projectLen = c.execute('''SELECT * FROM "project" ''')
        for project in range(0, len(projectLen.fetchall())):
            position = random.choice(positionList)
            salaryProject = 2000
            bonus = np.random.randint(100, high=500)
            finalSalary = salary + salaryProject + bonus
            
            c.execute('''INSERT INTO "participate"("employeeid","projectid", "position", "salaryProject", "bonus", "finalSalary") VALUES (?,?,?,?,?,?)''', 
                      [employee+1, project +1, position, salaryProject, bonus, finalSalary])
        
    # project = 30
    # projectId = np.random.randint(1, hight=projec)
    # c.execute('''INSERT INTO "project"("id") VALUES (?)''', projectId)
    
    # statusList = ["Đạt", "Không đạt"]
    # status = random.choice(statusList)
    # c.execute('''INSERT INTO "project"("status") VALUES (?)''', status)
 
    connect.commit()
    connect.close()