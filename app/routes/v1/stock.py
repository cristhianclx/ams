# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from forms.stock import StockForm
from models.user import User
from services.stock import StockService
from utils.database import get__database
from utils.auth import get_current_active_user


router = APIRouter()

service = StockService()


@router.get("/{code}/", response_model=StockForm)
def get(code: str, db: Session = Depends(get__database), current_user: User = Depends(get_current_active_user)):
    """
    to get stock data
    """
    stock = service.get(code, db)
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_DOES_NOT_EXIST,
            detail="Stock doesn't exist",
        )
    return stock
