# -*- coding: utf-8 -*-

from db.schemas import Base

from typing import Optional
from pydantic import (
    EmailStr,
    validator,
)

from utils.auth import get_password_hash


USER_PASSWORD_MIN_LENGTH = 6


class UserBaseForm(Base):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr


class UserForm(UserBaseForm):
    password: str

    @validator("password")
    def password_validate(cls, v) -> str:  # pylint: disable=no-self-argument
        if len(v) < USER_PASSWORD_MIN_LENGTH:
            raise ValueError("password needs to have at least {} characters".format(USER_PASSWORD_MIN_LENGTH))
        v = get_password_hash(v)
        return v


class UserLoginForm(Base):
    email: EmailStr
    password: str

    @validator("password")
    def password_validate(cls, v) -> str:  # pylint: disable=no-self-argument
        if len(v) < USER_PASSWORD_MIN_LENGTH:
            raise ValueError("password needs to have at least {} characters".format(USER_PASSWORD_MIN_LENGTH))
        return v
