# -*- coding: utf-8 -*-

from db.schemas import Base


class StockForm(Base):
    code: str
    name: str
