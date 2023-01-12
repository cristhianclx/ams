# -*- coding: utf-8 -*-

from db.engine import SessionLocal
from models.stock import Stock
from repositories.stock import StockRepository


class StockService:
    def __init__(self) -> None:
        self.repository = StockRepository

    def get(
        self,
        code: str,
        session: SessionLocal,
    ) -> Stock:
        repo = self.repository(session)
        return repo.get(reference=code)
