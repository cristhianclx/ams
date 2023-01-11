# -*- coding: utf-8 -*-

from typing import List


##
# configuration
##

ALLOWED_HOSTS: List[str] = ["*"]

NAME: str = "api-market-stock.demo.pe"

VERSION: str = "v1"


##
# auth
##

SECRET_KEY = "e5db3a0ac29c4eafb342ce13110be93e5307e1b1fd6c623b75a27fc8e7793c4b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


##
# stage
##

STAGE: str = "-"


##
# static
##

STATIC_DIR: str = "static"


##
# templates
##

TEMPLATES_DIR: str = "templates"
