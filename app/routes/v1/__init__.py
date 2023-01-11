# -*- coding: utf-8 -*-

from fastapi import APIRouter

from routes.v1.stock import router as router__stock
from routes.v1.user import router as router__user
from utils.constants import responses


router = APIRouter()

router.include_router(
    router__stock,
    prefix="/stocks",
    tags=["stocks"],
    responses=responses,
)
router.include_router(
    router__user,
    prefix="/users",
    tags=["users"],
    responses=responses,
)
