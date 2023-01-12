# -*- coding: utf-8 -*-

from typing import Any, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from forms.stock import StockForm
from services.stock import StockService
from sqlalchemy.orm import Session
from utils.cache import get_api_usage
from utils.database import get__database

router = APIRouter()

service = StockService()


@router.get("/{code}/", response_model=StockForm)
def get(
    code: str,
    session: Session = Depends(get__database),
    user_with_api_usage: Tuple = Depends(get_api_usage),
) -> Any:
    """
    to get stock data
    """
    stock = service.get(code, session)
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_DOES_NOT_EXIST,
            detail="Stock doesn't exist",
        )
    return stock
