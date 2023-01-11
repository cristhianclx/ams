# -*- coding: utf-8 -*-

from settings.base import *  # pylint: disable=wildcard-import,unused-wildcard-import

##
# stage
##

STAGE: str = "docker"

##
# database
##

DATABASE_URL: str = "postgresql://api:password@database:5432/bbdd"
