# -*- coding: utf-8 -*-

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from routes import base, v1
from settings.active import (  # noqa: F401 # pylint: disable=unused-import
    ALLOWED_HOSTS,
    NAME,
    STAGE,
    STATIC_DIR,
    TEMPLATES_DIR,
    VERSION,
)

app: FastAPI = FastAPI(
    debug=True,
    title=f"{NAME} - {STAGE}",
    redoc_url=None,
    version=f"{VERSION}",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routes
app.include_router(base.router, tags=["base"])
app.include_router(v1.router, prefix="/v1")


# /
@app.get("/", include_in_schema=False)
def root() -> Any:
    """
    /
    """
    return RedirectResponse("/docs")


# /robots.txt
@app.get("/robots.txt", include_in_schema=False)
def robots_txt() -> Any:
    """
    robots.txt to now allow spiders
    """
    return FileResponse(f"{TEMPLATES_DIR}/robots.txt")


# /favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
def favicon_ico() -> Any:
    """
    favicon.ico
    """
    return FileResponse("{STATIC_DIR}/ico/favicon.ico")
