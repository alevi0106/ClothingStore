from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from .settings import JWTConf


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
DB = None # DB access file


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWTConf.ACCESS_TOKEN_EXPIRE_MINUTES.value)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWTConf.SECRET_KEY.value, algorithm=JWTConf.ALGORITHM.value)
    return encoded_jwt


def authenticate_user(username: str, password: str):
    user = DB.get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_user_from_token(token: str):
    payload = jwt.decode(token, JWTConf.SECRET_KEY.value, algorithms=[JWTConf.ALGORITHM.value])
    return payload.get("sub")
