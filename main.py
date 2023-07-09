from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import appDes as appDes
import pandas as pd
from sql_app import models, data
from database import SessionLocal, engine, get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

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

@app.get('/project/LuongCuaNhanVien/{employeeid}', 
         tags=['Hoàng Anh Pandas'],
         description=appDes.descriptionApi['HoangAnhPandas']['LuongCuaNhanVien'])
def get_employee_salary_project(
    employeeid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if( employeeid != None):
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