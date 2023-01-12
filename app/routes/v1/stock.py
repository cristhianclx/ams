# -*- coding: utf-8 -*-

from typing import Any, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from forms.stock import StockForm
from models.user import User
from services.stock import StockService
from sqlalchemy.orm import Session
from utils.alpha_vantage import AlphaVantageCache
from utils.cache import get_api_usage
from utils.database import get__database

router = APIRouter()

service = StockService()


@router.get("/{code}/")
def get(
    code: str,
    session: Session = Depends(get__database),
    user_with_api_usage: Tuple[User, dict] = Depends(get_api_usage),  # pylint:disable=unused-argument
) -> Any:
    """
    to get stock data
    """
    stock = service.get(code, session)
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock doesn't exist",
        )
    context = StockForm.from_orm(stock).dict()
    context["price"] = AlphaVantageCache().get_data(code)
    return context
