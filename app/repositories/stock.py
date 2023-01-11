# -*- coding: utf-8 -*-

from db.engine import SessionLocal
from models.stock import Stock
from repositories.base import AbstractRepository


class StockRepository(AbstractRepository):

    def __init__(self, session: SessionLocal):
        self.model = Stock
        self.session = session
        
    def get(self, code: str) -> Stock:
        return self.session.query(self.model).filter(
            self.model.code == code,
        ).first()
