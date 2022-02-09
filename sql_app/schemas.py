# coding=utf-8
'''
Created on 2022/2/8 4:27 下午
__author__=yh
__remark__=
'''

from typing import List, Optional

from pydantic import BaseModel



class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    deptid:int


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserInfo(User):
    deptid:int
    deptname:str


# Item 的基类,表示创建和查询 Item 时共有的属性
class DeptBase(BaseModel):
    id: int
    username: str
    deptid: int
    deptname:str


# 创建 Item 时的 Model
class DeptCreate(DeptBase):
    pass


# 查询 Dept 时的 Model
class Dept(DeptBase):
    id: int
    userid: int
    deptid: int
    deptname:str

    # 向 Pydantic 提供配置
    class Config:
        #  orm_mode 会告诉 Pydantic 模型读取数据，即使它不是字典，而是 ORM 模型（或任何其他具有属性的任意对象）
        orm_mode = True

