# -*- coding: utf-8 -*-

from fastapi import APIRouter


router = APIRouter()


@router.get("/ping/", summary="ping")
def ping():
    """
    ping status for system, to know everything is working OK
    """
    context = {
        "message": "pong",
    }
    return context
