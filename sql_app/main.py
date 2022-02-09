# coding=utf-8

'''
Created on 2022/2/8 4:27 下午
__author__=yh
__remark__=
'''

from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, Path, Query, Body
from sqlalchemy.orm import Session
from models import Base
from schemas import User, UserCreate,UserInfo
from database import SessionLocal, engine
from sql_app import curd

Base.metadata.create_all(bind=engine)

app = FastAPI()


# 依赖项,获取数据库会话对象
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 创建用户
@app.post("/create", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1、先查询用户是否有存在
    db_user = curd.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user 已存在")
    res_user = curd.create_user(db, user)
    return res_user


# 根据 user_id 获取用户
@app.get("/user_id/{user_id}", response_model=User)
async def get_user(user_id: int = Path(...), db: Session = Depends(get_db)):
    return curd.get_user(db, user_id)


# 根据 username 获取用户
@app.get("/user_name/{username}", response_model=User)
async def get_user_by_username(username: str = Path(...), db: Session = Depends(get_db)):
    return curd.get_user_by_username(db, username)


# 获取所有用户
@app.get("/users_all/", response_model=List[User])
async def get_users(skip: int = Query(0),
                    limit: int = Query(100),
                    db: Session = Depends(get_db)):
    return curd.get_users(db, skip, limit)

#根据用户id获取用户部门信息
@app.get("/users/userinfo/{username}")
async def get_user_info(username: str = Path(...), db: Session = Depends(get_db)):
    return curd.get_userinfo(db,username)


# 创建 item
# @app.post("/create/{user_id}/", response_model=Item)
# async def get_user_item(user_id: int = Path(...), item: ItemCreate = Body(...), db: Session = Depends(get_db)):
#     return curd.create_user_item(db, item, user_id)
#
#
# # 获取所有 item
# @app.get("/items/", response_model=List[Item])
# async def get_items(skip: int = Query(0),
#                     limit: int = Query(100),
#                     db: Session = Depends(get_db)):
#     return curd.get_items(db, skip, limit)
#
#
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True, debug=True)