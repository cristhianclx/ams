# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse

from routes import base
from routes import v1
from settings.active import ALLOWED_HOSTS
from settings.active import NAME
from settings.active import STAGE
from settings.active import STATIC_DIR
from settings.active import TEMPLATES_DIR
from settings.active import VERSION


app: FastAPI = FastAPI(
    debug=True,
    title="{} - {}".format(NAME, STAGE),
    redoc_url=None,
    version="{}".format(VERSION),
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
async def root():
    """
    /
    """
    return RedirectResponse("/docs")


# /robots.txt
@app.get("/robots.txt", include_in_schema=False)
async def robots_txt():
    """
    robots.txt to now allow spiders
    """
    return FileResponse("{}/robots.txt".format(TEMPLATES_DIR))


# /favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    """
    favicon.ico
    """
    return FileResponse("{}/ico/favicon.ico".format(STATIC_DIR))
