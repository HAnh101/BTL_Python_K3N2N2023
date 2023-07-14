import sqlite3
import numpy as np 
import random
import string

def initDef():
    connect = sqlite3.connect('LuongNhanVien.db')
    c = connect.cursor()

    # c.execute('''DROP TABLE "employee"''')
    # c.execute('''DROP TABLE "department"''')
    # c.execute('''DROP TABLE "participate"''')
    # c.execute('''DROP TABLE "project"''')

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

    def departmentIsReady(departmentId, employeeEachDepartment, department):
        employeeInDepartment = c.execute('''SELECT * FROM "employee" WHERE departmentId == ?''', [departmentId])
    
        if(len(employeeInDepartment.fetchall()) < employeeEachDepartment):
            return departmentId
        else:
            departmentIdNew = np.random.randint(0,high=len(listDepartment)+1)
            employeeEachDepartmentNew = employeeEachDepartment
            departmentNew = department
            return departmentIsReady(departmentIdNew, employeeEachDepartmentNew, departmentNew)
        
    salary = 10000
    
    def setEmployeeToDepartment(departmentId):
        firstName = firstNameList[int(np.floor(len(firstNameList) * np.random.random()))]
        middleName =  middleNameList[int(np.floor(len(middleNameList) * np.random.random()))]
        lastName = random.choices(string.ascii_uppercase, k=1)
        rate = np.random.randint(1, high=5)
        c.execute('''INSERT INTO "employee"("name", "departmentId", "salary", "rate") VALUES (?, ?, ?, ?)''', [f'{firstName} {middleName} {lastName[0]}', departmentId, salary, rate])

    for eachEmployee in range (0, employeeSum):
        departmentId = np.random.randint(0,high=len(listDepartment)+1)
        setEmployeeToDepartment(departmentIsReady(departmentId, employeeEachDepartment, department))

    listProject = [
        ["App quản lí công việc"],
        ["App quản lí thời gian"],
        ["App thi trắc nghiệm bằng lái xe máy"],
        ["App quản lí chi tiêu"],
        ["App nhật kí nấu ăn"],
        ["App chạy bộ"],
        ["App học từ vựng tiếng Anh"],
        ["App quản lý danh bạ"],
        ["App ghi chép"],
        ["App dự báo thời tiết"]
    ]
    statusList = ["Hoàn thành", "Chưa hoàn thành"]
    
    def setProject(index):
        name = listProject[index]
        status = statusList[int(np.floor(len(statusList) * np.random.random()))]
        c.execute('''INSERT INTO "project"("name", "status") VALUES (?, ?)''', [ f'{name}', status])

    
    for eachProject in range(0, len(listProject)):
        setProject(eachProject)

    positionList = ["Trưởng nhóm", "Thành viên"]

    for employee in range(0, employeeSum):
        for projectEachEmployee in range(0,3):
            projectLen = c.execute('''SELECT * FROM "project" ''')
            project = int(np.floor(len(listProject) * np.random.random()))
            position = random.choice(positionList)
            salaryProject = 2000
            if(position == "Trưởng nhóm"):
                bonus = np.random.randint(300, high=500)
            else:
                bonus = np.random.randint(100,high=300)
            finalSalary = salary + salaryProject + bonus
            
            c.execute('''INSERT OR REPLACE INTO "participate"("employeeid","projectid", "position", "salaryProject", "bonus", "finalSalary") VALUES (?,?,?,?,?,?)''', 
                        [employee+1, project+1, position, salaryProject, bonus, finalSalary])


    connect.commit()
    connect.close()