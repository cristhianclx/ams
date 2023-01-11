# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column,
    String,
)

from db.orm import ModelBase


class Stock(ModelBase):
    __tablename__: str = "stocks"

    code = Column(String(10), primary_key=True, nullable=False,)
    name = Column(String, nullable=False)
