# -*- coding: utf-8 -*-

from datetime import (
    datetime,
    timedelta,
)

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Union

from models.user import User
from settings import (
    ALGORITHM,
    SECRET_KEY,
)
from utils.database import get__database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    username: Union[str, None] = None
    

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    from services.user import UserService
    service = UserService()
    user = service.get(db, email)
    if not user:
        return False
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get__database)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not decode credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(db, token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
