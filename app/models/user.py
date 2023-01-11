# -*- coding: utf-8 -*-

from db.orm import ModelBase
from sqlalchemy import Boolean, Column, String


class User(ModelBase):
    __tablename__: str = "users"

    email = Column(String, primary_key=True, index=True, nullable=False)
    first_name = Column(
        String,
        index=True,
        nullable=False,
    )
    last_name = Column(
        String,
        index=True,
        nullable=False,
    )
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
