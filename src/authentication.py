import logging
import datetime
from passlib.context import CryptContext
from jose import jwt
from typing import Dict, Optional, Union

from src.settings import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY, DOMAIN_URL

logger = logging.getLogger()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(email: str, expires_minutes: Optional[int] = None):
    to_encode: Dict[str, Union[str, datetime.datetime]] = {"sub": email}
    if expires_minutes:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def extract_id_from_token(token: str) -> str:
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload.get("sub")


def create_email_confirmation_link(email: str):
    token = create_access_token(email, expires_minutes=10)
    confirmation_link = "http://" + DOMAIN_URL.strip("/") + "/confirmaccount/" + token
    return confirmation_link
