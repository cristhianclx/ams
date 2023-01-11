# -*- coding: utf-8 -*-

from db.engine import SessionLocal
from forms.stock import StockForm
from repositories.stock import StockRepository


class StockService:
    def __init__(self) -> None:
        self.repository = StockRepository
        self.schema = StockForm

    def get(
        self,
        code: str,
        db: SessionLocal,
    ) -> StockForm:
        repo = self.repository(db)
        return repo.get(code=code)
