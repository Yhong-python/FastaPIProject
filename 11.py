# coding=utf-8
'''
Created on 2022/2/7 2:55 下午
__author__=yh
__remark__=
'''


# 导入 CryptContext
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional

# 常量池
# 通过 openssl rand -hex 32 生成的随机密钥
SECRET_KEY = "a425b52f41c6e28fb16a6484180da5f99276495d51591813d3340c91308fa776"
# 加密算法
ALGORITHM = "HS256"
# 过期时间，分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 600

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


# 密码加密
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# print(hash_password('fakehashedsecret'))


# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# print(verify_password('87871526',hash_password('87871526')))

# 模拟数据库
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$KJfxiTG/iUiZhFnzSTGxxekiSq7mNpM0myN.shNHGkWfD7Cm0.HBW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    }
}

# 返回给客户端的 User Model，不需要包含密码
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


# 继承 User，用于密码验证，所以要包含密码
class UserInDB(User):
    hashed_password: str

# 模拟从数据库中根据用户名查找用户
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
# print(get_user(fake_users_db,'johndoe'))

# 根据用户名、密码来验证用户
def authenticate_user(db, username: str, password: str):
    # 1、通过用户名模拟去数据库查找用户
    user = get_user(db, username)
    if not user:
        # 2、用户不存在
        return False
    if not verify_password(password, user.hashed_password):
        # 3、密码验证失败
        return False
    # 4、验证通过，返回用户信息
    return user
print(authenticate_user(fake_users_db,'johndoe','fakehashedsecret'))

# 返回给客户端的 Token Model
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


