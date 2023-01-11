# -*- coding: utf-8 -*-

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from forms.user import UserBaseForm, UserForm, UserLoginForm
from services.user import UserService
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from utils.auth import authenticate_user, create_access_token
from utils.database import get__database

router = APIRouter()

service = UserService()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(item: UserForm, db: Session = Depends(get__database)):
    """
    to create a new user with a token
    """
    if service.get(db, item.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    user = service.create(db, item)
    context = UserBaseForm(user.dict())
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
        },
        expires_delta=access_token_expires,
    )
    context["login"] = {
        "token": access_token,
    }
    return context


@router.post("/login/")
def login(item: UserLoginForm, db: Session = Depends(get__database)):
    """
    to login and get a token
    """
    user = service.get(db, item.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    user = authenticate_user(db, item.email, item.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
        },
        expires_delta=access_token_expires,
    )
    return {
        "login": {
            "token": access_token,
        }
    }
