# coding=utf-8
'''
Created on 2022/2/8 4:27 下午
__author__=yh
__remark__=
'''

from sqlalchemy.orm import Session
from sql_app.models import User
from sql_app.models import Dept
from sql_app.schemas import UserCreate,DeptCreate


# 根据 id 获取 user
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# 根据 email 获取 user
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()



# 获取所有 user
def get_users(db: Session, size: int = 0, limit: int = 100):
    return db.query(User).offset(size).limit(limit).all()


# 创建 user，user 类型是 Pydantic Model
def create_user(db: Session, user: UserCreate):
    dept_info={"1":"部门1","2":"部门2"}
    fake_hashed_password = user.password + "superpolo"
    # 1、使用传进来的数据创建 SQLAlchemy Model 实例对象
    db_user = User(username=user.username, hashed_password=fake_hashed_password)
    dept_info=Dept(username=user.username,deptid=user.deptid,deptname=dept_info.get(str(user.deptid)))
    # 2、将实例对象添加到数据库会话 Session 中
    db.add(db_user)
    db.add(dept_info)
    # 3、将更改提交到数据库
    db.commit()
    # 4、刷新实例，方便它包含来自数据库的任何新数据，比如生成的 ID
    db.refresh(db_user)
    return db_user


# 获取所有 item
def get_items(db: Session, size: int = 0, limit: int = 100):
    return db.query(Dept).offset(size).limit(limit).all()


# 创建 dept，dept 类型是 Pydantic Model
def create_item(db: Session, dept: DeptCreate):
    db_item = Dept(**dept.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 获取用户信息
def get_userinfo(db: Session, username: str):
    r=db.query(User.id,User.username,Dept.deptid,Dept.deptname).join(Dept,User.username==Dept.username).filter(User.username == username).first()
    print(type(r))
    print(r.id)
    return r