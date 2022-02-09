# coding=utf-8
'''
Created on 2022/2/7 3:43 下午
__author__=yh
__remark__=
'''

from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
# 导入 CryptContext
from passlib.context import CryptContext
# 导入 JWT 相关库
from jose import JWTError, jwt

# 常量池
# 通过 openssl rand -hex 32 生成的随机密钥
SECRET_KEY = "dc393487a84ddf9da61fe0180ef295cf0642ecbc5d678a1589ef2e26b35fce9c"
# 加密算法
ALGORITHM = "HS256"
# 过期时间，分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 模拟数据库
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$KJfxiTG/iUiZhFnzSTGxxekiSq7mNpM0myN.shNHGkWfD7Cm0.HBW",
        "disabled": False,
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


# 获取 token 路径操作函数的响应模型
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# 实例对象池
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


# 密码加密
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 模拟从数据库中根据用户名查找用户
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


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


# 用户名、密码验证成功后，生成 token
def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # 加密
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# OAuth2 获取 token 的请求路径
@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1、获取客户端传过来的用户名、密码
    username = form_data.username
    password = form_data.password
    # 2、验证用户
    user = authenticate_user(fake_users_db, username, password)
    if not user:
        # 3、验证失败，返回错误码
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 4、生成 token
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    # 5、返回 JSON 响应
    return {"access_token": access_token, "token_type": "bearer"}


# 根据当前用户的 token 获取用户，token 已失效则返回错误码
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1、解码收到的 token
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # 2、拿到 username
        username: str = payload.get("sub")
        if not username:
            # 3、若 token 失效，则返回错误码
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # 4、获取用户
    user = get_user(fake_users_db, username=token_data.username)
    if not user:
        raise credentials_exception
    # 5、返回用户
    return user


# 判断用户是否活跃，活跃则返回，不活跃则返回错误码
async def get_current_active_user(user: User = Depends(get_current_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User")
    return user


# 获取当前用户信息
@app.get("/user/me")
async def read_user(user: User = Depends(get_current_active_user)):
    return user


# 正常的请求
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


if __name__ == '__main__':
    uvicorn.run(app="验证用户:app", reload=True, host="127.0.0.1", port=8080)