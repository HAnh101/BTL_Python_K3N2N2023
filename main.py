from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Union
import appDes as appDes
import numpy as np
import pandas as pd
import sql_app.models as models
import sql_app.schemas as schemas
import sql_app.data as data
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine, get_db
from sql_app.default import initDef 
from fastapi.responses import HTMLResponse
import webbrowser
import os

templates = Jinja2Templates(directory="pages/")
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quản lý luơng nhân viên",
    description=appDes.description,
    version="1.0.0",
    contact={
        "maNV": "Source Code",
        "url": "https://github.com/HAnh101/BTL_Python_K3N2N2023",
    },
    openapi_tags=appDes.tags_metadata
)

# initDef()

@app.get('/', response_class=HTMLResponse, tags=['Trang chủ'])
def home():
    html_content = '''
    <html>
        <head>
            <title>BTL Python K3N2</title>
            <style>
                h1{
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Bài tập lớn môn Lập trình Python</h1>
            <br> </br>
            <div>
                <h2>Nhóm gồm 4 thành viên:</h2>
                <ul>
                    <li>A39482 Nguyễn Ngọc Anh</li>
                    <li>A38303 Phùng Thị Diệu Linh</li>
                    <li>A38207 Nguyễn Thị Lan</li>
                    <li>A37672 Trần Hoàng Anh</li>
                </ul>
            </div>
        </body>
    </html>
    '''
    return HTMLResponse(content=html_content, status_code=200)

#region Hoang Anh
#pd

@app.get('/project/LuongCuaNhanVien/{employeeid}', 
         tags=['Hoàng Anh Pandas'],
         description=appDes.descriptionApi['HoangAnhPandas']['LuongCuaNhanVien'])
def get_employee_salary_project(
    employeeid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if(employeeid != None):
        if employeeid > 0:
            employeeInDepartment = data.ProjectAndEmployeeMethod.get_all_employee(db, employeeid=employeeid)
            df = pd.DataFrame.from_dict(employeeInDepartment)
            df['Tổng lương tháng'] = df['Tổng lương tháng']
            luong = df['Tổng lương tháng'].tolist()
            project = df['Dự án'].to_list()
            maNV = df['Mã nhân viên'][0]
            project.insert(0, 'Mã nhân viên')
            luong.insert(0, maNV)
            dataframe = pd.DataFrame(data = luong, index= project)
            print(dataframe.T)
            return dataframe
        else:
            raise HTTPException(status_code=404, detail={
            "field": "employeeid",
            "errMsg": "Thông tin không hợp lệ"
        })
            
    else: 
        raise HTTPException(status_code=404, detail={
            "field": "employeeid",
            "errMsg": "Chưa có thông tin"
        })


@app.post('/project/CapNhatDuAn', 
          tags=['Hoàng Anh Pandas'],
          description=appDes.descriptionApi['HoangAnhPandas']['CapNhatDuAn'])
def post_project(project: schemas.Project, db : Session = Depends(get_db)):
    result = " "
    if project.projectid >0 :
        updateData = data.ProjectMethod.update_project(db, schemas.Project(
            projectid= project.projectid,
            projectName= project.projectName,
            projectStatus= project.projectStatus,
            ))
        result = data.ProjectMethod.get_project(db, project.projectid)
    else:
        result = {
            "field": "deparmentid",
            "errMsg": "Thông tin không hợp lệ"
        }
    return result

#np
@app.get('/project/LuongTrungBinhDuAn/{projectid}', 
         tags= ['Hoàng Anh Numpy'], 
         description=appDes.descriptionApi['HoangAnhNumpy']['LuongTrungBinhDuAn'])
def get_Project_Avg_Salary(
    projectid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if projectid > 0 :
        ProjectSalary = data.ProjectAndEmployeeMethod.get_project_salary(db, projectid= projectid)
        df = pd.DataFrame.from_dict(ProjectSalary)
        project = df['Dự án'][0]
        luongTK= np.array([df['Tổng lương tháng']])
        luong = np.round(np.mean(luongTK), 1)
        return f'Lương trung bình của nhân viên trong dự án {project} là {luong}'
    else:
        raise HTTPException(status_code=404, detail={
            "field": "projectid",
            "errMsg": "Thông tin không hợp lệ"
            })


@app.post('/project/TongHaiDuAn', tags= ['Hoàng Anh Numpy'],
          description=appDes.descriptionApi['HoangAnhNumpy']['TongHaiDuAn'])
def Sum_2_project(
    employee: schemas.sum2Project,
    db: Session = Depends(get_db)
):
    if employee.employeeid != None or employee.project1 != None or employee.project2 != None :
        if employee.employeeid > 0 :
            if employee.project1 > 0 and employee.project2 >0:
                projectSalary1= data.ParticipateMethod.get_employee_projectSalary(db, schemas.ParticipateBase(employeeId=employee.employeeid, projectId=employee.project1))
                projectSalary2= data.ParticipateMethod.get_employee_projectSalary(db, schemas.ParticipateBase(employeeId=employee.employeeid, projectId=employee.project2))
                df1 = pd.DataFrame.from_dict(projectSalary1)
                df2 = pd.DataFrame.from_dict(projectSalary2)
                luongDuAn1 = df1['Lương tháng'][0]
                luongDuAn2 = df2['Lương tháng'][0]
                duAn1 = df1['Dự án'][0]
                duAn2 = df2['Dự án'][0]
                name = df1['Họ tên'][0]
                luong = np.array([luongDuAn1, luongDuAn2])
                luongTrungBinh = np.round(np.sum(luong) ,1)
            else:
                raise HTTPException(status_code=404, detail={
                "field": "duAn1, duAn2",
                "errMsg": "Thông tin không hợp lệ"
                })
        else: 
            raise HTTPException(status_code=404, detail={
            "field": "employeeid",
            "errMsg": "Thông tin không hợp lệ"
            })
    else:
        raise HTTPException(status_code=404, detail={
            "field": "employeeid, duAn1, duAn2",
            "errMsg": "Chưa có thông tin"
        })
    return f'Tổng lương {duAn1} và {duAn2} của nhân viên {name} là {luongTrungBinh}'




# endregion
#region Ngoc Anh
#pd

@app.get('/project/ThongKeLuongThuongThang/{projectid}', 
        tags=['Ngọc Anh Pandas'], 
        description=appDes.descriptionApi['NgocAnhPd']['ThongKeLuongThuongThang'])
def get_bonus_project(
    projectid: int, 
    db: Session = Depends(get_db)
):
    if(projectid > 0) :
        getProject = data.ProjectMethod.get_project_id(db, id=projectid)
        if projectid > len(getProject):
            return {
                "msg": "Không tồn tại dự án"
            }
        else:
            listBonusProject = data.BonusProjectMethod.get_all_bonus(db, projectid)
            if len(listBonusProject) != 0:
                df = pd.DataFrame.from_dict(listBonusProject)
                bonusList = df.groupby(df['Lương thưởng']).mean(numeric_only = True)
                projectName = df['Dự án'][0]
                return {
                    "msg": f"Thống kê lương thưởng theo dự án {projectName}",
                    "data" : bonusList.T
                }
            else:
                return {
                    "msg": "Không tồn tại bản ghi nào"
                }
    else:
        raise HTTPException(status_code=404, detail={
                "field" : "projectid",
                "errMsg" : "Giá trị projectid không thể nhỏ hơn hoặc bằng 0"
            })

@app.post('/department/TimKiemNhanVien', tags=['Ngọc Anh Pandas'], description=appDes.descriptionApi['NgocAnhPd']['TimKiemNhanVien'])
def post_find_employee(employeeInfor: schemas.EmployeeFind, db: Session = Depends(get_db)):
    result = ""
    errorList = []
    line = 0
    # for dict in employeeInfor:
    #     if(line >= 2):
    #         if dict[1] < 0:    
    #             errorList.append({"field": dict[0], "errMsg" : "Lương nhỏ hơn 0"})
    #         elif dict[1] > 10:
    #             errorList.append({"field": dict[0], "errMsg" : "Lương lớn hơn 10"})
    #     else:
    #         if line!=1:
    #             if dict[1] <= 0:    
    #                 errorList.append({"field": dict[0], "errMsg" : "id Không được nhỏ hơn hoặc bằng 0"})
    #     line +=1
    if len(errorList) > 0:
        result = errorList
    else:
        list_avai = data.EmployeeInformationMethod.find_employee(db, employeeInfor)
        if(len(list_avai) !=0): 
            df = pd.DataFrame.from_dict(list_avai)
            dfsize = len(df.index)
            result = {
                "msg" : f"có {dfsize} kết quả phù hợp",
                "data" : df.T
            }
        else:
            result = {
                "msg": "không có kết quả phù hợp"
            }
    return result

@app.get('/project/LuongTongKetThangCuaNhanVien', tags=['Ngọc Anh Numpy'], description = appDes.descriptionApi['NgocAnhNp']['LuongTongKetThangCuaNhanVien'])
def get_salary_project_sum_employee(
    employeeid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if( employeeid != None):
        if(employeeid >0):
            employeeIndepartment = data.SalaryProjectSumMethod.get_all_employee(db, employeeid=employeeid);
            if np.array(employeeIndepartment).size !=0:
                df = pd.DataFrame.from_dict(employeeIndepartment)

                tongLuongDuAn = (df['Tổng lương trong dự án'].sum()).tolist()
                empId = df['Mã nhân viên'][0]
                return {
                    "msg": f'Tổng lương trong dự án {empId} là: {tongLuongDuAn}',
                    "data": tongLuongDuAn}
            else :
                raise HTTPException(status_code=404, detail={
                    "field": "employeeid",
                    "errMsg": "Không tồn tại nhân viên này!"
                }) 
        else:
            raise HTTPException(status_code=404, detail={
                "field": "employeeid",
                "errMsg": "Phải lớn hơn 0"
            })
    else: 
        raise HTTPException(status_code=404, detail={
            "field": "employeeid",
            "errMsg": "Chưa có thông tin"
        })

@app.post('/project/CapNhatLuongTheoThang', tags=['Ngọc Anh Numpy'], description = appDes.descriptionApi['NgocAnhNp']['CapNhatLuongTheoThang'])
def post_update_salary(salaryList: schemas.ProjectSalaryUpdate ,db: Session = Depends(get_db)):
    result = ""
    errorList = []
    line = 0
    for dict in salaryList:
        if(line >= 2):
            if dict[1] < 0:    
                errorList.append({"field": dict[0], "errMsg" : "Lương nhỏ hơn 0"})
            elif dict[1] >100000:
                errorList.append({"field": dict[0], "errMsg" : "Lương lớn hơn 10"})
        else:
            if dict[1] <= 0:    
                errorList.append({"field": dict[0], "errMsg" : "id Không được nhỏ hơn hoặc bằng 0"})
        line +=1
    if len(errorList) > 0:
        result = errorList
    else:
        if np.array(data.ProjectEmployeeMethod.get_employee(db, schemas.ProjectEmployeeBase(employeeid=salaryList.employeeid, projectid=salaryList.projectid))).size != 0:
            salaryCal = np.round(
                (salaryList.employeeSalary) + 
                (salaryList.projectSalary)
                , 2)
            updateData = data.ProjectEmployeeMethod.update_point(db, schemas.SubjectStudentPointCreate(
                employeeId=salaryList.employeeid,
                projectId=salaryList.projectid,
                employeeSalary = salaryList.employeeSalary,
                projectSalary = salaryList.projectSalary,
                finnalSalary = np.round(((salaryList.employeeSalary + salaryList.projectSalary)),1)
                ))
            result = {
                "Họ và tên": data.EmployeeMethod.get_by_id(db, salaryList.employeeid)[0].name,
                "Dự án" : data.ProjectMethod.ProjectMethod(db, salaryList.projectid)[0].name,
                "Điểm": updateData.finnalSalary
            }
        else:
            if np.array(data.ProjectMethod.ProjectMethod(db, salaryList.projectid)).size == 0:
                result = {
                    "field": "projectid",
                    "errMsg" : "Không tồn tại dự án"
                }
            elif np.array(data.EmployeeMethod.get_by_id(db, employeeid = salaryList.employeeid)).size == 0:
                result = {
                    "field": "employeeid",
                    "errMsg" : "Không tồn tại nhân viên"
                }

    return result

# endregion

# Region Linh
#np
@app.get('/statistic/ranking',
         tags = ['Linh Numpy'],
         description=appDes.descriptionApi['LinhNP']['BangXepHang'])

def get_ranking(
    db: Session = Depends(get_db)
):
    salaryAndRateBoard = data.FinalSalaryAndRate.get_list(db)
    df = pd.DataFrame.from_dict(salaryAndRateBoard)
    df['Xếp loại'] = get_evaluation(df['Đánh giá'])
    table = pd.DataFrame.from_dict(df).to_html()
    text_file = open("employee_list.html", "w", encoding='utf8')
    text_file.write(table)
    text_file.close()
    webbrowser.open(os.getcwd() + '/employee_list.html')
    
    return HTMLResponse(content=table, status_code=200)

@np.vectorize
def get_evaluation(rate):
    if rate == 5: 
        return 'Xuất sắc'
    elif rate > 2:
        return 'Tốt'
    else:
        return 'Trung bình'
    
@app.post('/Update/Rate',
         tags = ['Linh Numpy'],
         description=appDes.descriptionApi['LinhNP']['CapNhatDanhGiaNhanVien'])
def updateRate(
    employee: schemas.EmployeeRate,
    db: Session = Depends(get_db)
):
    result = " "
    if(employee.id > 0):
        updateRate = data.EmployeeMethod.update_rate(db,schemas.EmployeeRate(
            id = employee.id,
            rate = employee.rate
        ))
        result = data.EmployeeMethod.get_rate(db, employee.id)
    else:
        result = {
            "field": "classid",
            "errMsg": "Thông tin không hợp lệ"
        }
    return result
#pd

@app.get('/statistic/top10',
         tags = ['Linh Pandas'],
         description=appDes.descriptionApi['LinhPD']['DanhSachNhanVienTop'])
def get_top10(db: Session = Depends(get_db)):
    salaryBoard = data.FinalSalaryAndRate.get_listFinalSalary(db)
    df = pd.DataFrame.from_dict(salaryBoard).head(10)
    table = pd.DataFrame.from_dict(df).to_html()
    text_file = open("employee_list.html", "w", encoding='utf8')
    text_file.write(table)
    text_file.close()
    webbrowser.open(os.getcwd() + '/employee_list.html')
    
    return HTMLResponse(content=table, status_code=200)

@app.post('/Department/avgFinalSalary',
         tags = ['Linh Pandas'],
         description=appDes.descriptionApi['LinhPD']['LuongTrungBinhPhongBan'])
def avgFinalSalary(
    department: schemas.avgSalaryDepartment,
    db: Session = Depends(get_db)
):
    if(department.id != None):
        avgSalary = data.DepartmentMethod.get_avgFinalSalary_department(db, schemas.avgSalaryDepartment(id=department.id))
        df= pd.DataFrame.from_dict(avgSalary)
        nameD = df['Phòng ban'][0]
        LuongTB = df['Lương tháng trung bình'][0]
        
    else:
        result = {
            "field": "departmentId",
            "errMsg": "Thông tin không hợp lệ"
        }
    return f'Lương tháng trung bình của {nameD} là {LuongTB}'

# endRegion