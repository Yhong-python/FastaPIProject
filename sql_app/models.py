# coding=utf-8
'''
Created on 2022/2/8 4:27 下午
__author__=yh
__remark__=
'''
from sqlalchemy import Boolean, Column, ForeignKey, Integer,VARCHAR
from sqlalchemy.orm import relationship

from sql_app.database import Base


class User(Base):
    # 1、表名
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    # 2、类属性，每一个都代表数据表中的一列
    # Column 就是列的意思
    # Integer、String、Boolean 就是数据表中，列的类型
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(VARCHAR(32), unique=True, index=True)
    hashed_password = Column(VARCHAR(32))
    is_active = Column(Boolean, default=True)

    # items = relationship("Item", back_populates="owner")


class Dept(Base):
    __tablename__ = "depts"
    __table_args__ = {'extend_existing': True}

    # userid = Column(Integer, foreign_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(32), ForeignKey("users.username"))
    deptid = Column(Integer)
    deptname = Column(VARCHAR(32))
    # owner_id = Column(Integer, ForeignKey("users.id"))


    # owner = relationship("User", back_populates="items")
    # ALTER
    # TABLE
    # depts
    # CONVERT
    # TO
    # CHARACTER
    # SET
    # utf8;