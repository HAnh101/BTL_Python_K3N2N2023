from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app import appDes as appDes
from sql_app import models
from sql_app.database import SessionLocal, engine
from fastapi.responses import HTMLResponse
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quản lý luơng nhân viên",
    description=appDes.description,
    version="1.0.0",
    contact={
        "name": "Source Code",
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