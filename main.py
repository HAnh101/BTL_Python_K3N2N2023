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

#region Hanh
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
            project = df['Phòng ban'].to_list()
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