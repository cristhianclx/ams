# -*- coding: utf-8 -*-

from typing import Optional

from db.schemas import Base
from pydantic import EmailStr, validator
from utils.auth import get_password_hash

USER_PASSWORD_MIN_LENGTH = 6


class UserBaseForm(Base):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr


class UserForm(UserBaseForm):
    password: str

    @validator("password")
    def password_validate(cls, value: str) -> str:  # pylint:disable=no-self-argument
        if len(value) < USER_PASSWORD_MIN_LENGTH:
            raise ValueError(f"password needs to have at least {USER_PASSWORD_MIN_LENGTH} characters")
        value = get_password_hash(value)
        return value


class UserLoginForm(Base):
    email: EmailStr
    password: str

    @validator("password")
    def password_validate(cls, value: str) -> str:  # pylint:disable=no-self-argument
        if len(value) < USER_PASSWORD_MIN_LENGTH:
            raise ValueError(f"password needs to have at least {USER_PASSWORD_MIN_LENGTH} characters")
        return value
