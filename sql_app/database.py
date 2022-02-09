# coding=utf-8
'''
Created on 2022/2/8 4:27 下午
__author__=yh
__remark__=
'''

# 1、导入 sqlalchemy 部分的包
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 2、声明 database url

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# mysql-pymysql 库
SQLALCHEMY_DATABASE_URL="mysql+pymysql://root:yanghong1994@127.0.0.1:3306/fastapidb?charset=utf8mb4"

# 3、创建 sqlalchemy 引擎
# echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    encoding='utf8',
    # echo=True
)

# 4、创建一个 database 会话
# SQLAlchemy中，CRUD是通过会话进行管理的，所以需要先创建会话，
# 每一个SessionLocal实例就是一个数据库session
# flush指发送到数据库语句到数据库，但数据库不一定执行写入磁盘
# commit是指提交事务，将变更保存到数据库文件中
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5、返回一个 ORM Model
Base = declarative_base()