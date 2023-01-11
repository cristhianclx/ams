# -*- coding: utf-8 -*-

from db.orm import ModelBase
from sqlalchemy import Column, String


class Stock(ModelBase):
    __tablename__: str = "stocks"

    code = Column(
        String(10),
        primary_key=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
