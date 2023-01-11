# -*- coding: utf-8 -*-

from settings.base import *  # pylint: disable=wildcard-import,unused-wildcard-import

##
# stage
##

STAGE: str = "main"

##
# database
##

DATABASE_URL: str = "postgres://api:password@database:5432/bbdd"
