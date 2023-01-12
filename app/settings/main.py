# -*- coding: utf-8 -*-

from settings.base import *  # noqa:F401,F403 pylint:disable=wildcard-import,unused-wildcard-import
from ssm_parameter_store import EC2ParameterStore

SSM_REGION = "us-east-1"

store = EC2ParameterStore(region_name=SSM_REGION)


##
# stage
##

STAGE = "main"

parameters = store.get_parameters_with_hierarchy(f"/ams.demo.pe/{STAGE}/")


##
# database
##

DATABASE_URL: str = "postgresql://{}:{}@{}:{}/{}".format(  # pylint:disable=consider-using-f-string
    parameters["database"]["user"],
    parameters["database"]["password"],
    parameters["database"]["host"],
    parameters["database"]["port"],
    parameters["database"]["name"],
)


##
# cache
##

CACHE_URL: str = "redis://{}:{}/0".format(  # pylint:disable=consider-using-f-string
    parameters["cache"]["host"],
    parameters["cache"]["port"],
)


##
# API keys
##

ALPHA_VANTAGE_API_KEY: str = parameters["integrations"]["alpha-vantage-api-key"]
