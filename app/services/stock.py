# -*- coding: utf-8 -*-

from forms.stock import StockForm
from repositories.stock import StockRepository
from db.engine import SessionLocal


class StockService:

    def __init__(self) -> None:
        self.repository = StockRepository
        self.schema = StockForm
        
    def get(self, code: str, db: SessionLocal,) -> StockForm:
        repo = self.repository(db)
        return repo.get(code = code)
