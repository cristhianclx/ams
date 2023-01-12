# -*- coding: utf-8 -*-

from settings.base import *  # noqa: F401,F403 pylint: disable=wildcard-import,unused-wildcard-import

##
# stage
##

STAGE = "docker"

##
# database
##

DATABASE_URL: str = "postgresql://api:password@database:5432/bbdd"


##
# cache
##

CACHE_URL: str = "redis://cache:6379/0"


##
# API keys
##

ALPHA_VANTAGE_API_KEY: str = "DU42M4W3530FEJOB"
