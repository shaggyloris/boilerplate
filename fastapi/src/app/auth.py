from datetime import datetime, timedelta
from typing import Optional
import logging
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings
from .schemas import TokenData, NewUser, UserInDB
from .database import get_db

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2(flows={
    "password": {
        "tokenUrl": "/token",
        "scopes": {}
        }
    })


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )
    scheme, token = get_authorization_scheme_param(token)
    if not token or scheme.lower() != "bearer":
        raise credentials_exception
    try:
        headers = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise credentials_exception
    user = await get_local_user(token, db)
    return user

async def get_local_user(token: str, db):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user

def get_user(username: str, db) -> UserInDB:
    user = db.get_user(username)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def authenticate_user(username: str, password: str, db):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def add_user_to_db(user: NewUser, db) -> UserInDB:
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(username=user.username, hashed_password=hashed_password)
    db.add_user(db_user)
