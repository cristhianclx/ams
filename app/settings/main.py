# -*- coding: utf-8 -*-

from settings.base import *  # noqa: F401,F403 pylint: disable=wildcard-import,unused-wildcard-import
from ssm_parameter_store import EC2ParameterStore

SSM_REGION = "us-east-1"

store = EC2ParameterStore(region_name=SSM_REGION)


##
# stage
##

STAGE = "main"

parameters = store.get_parameters_with_hierarchy(f"/api-market-stock.demo.pe/{STAGE}/")


##
# database
##

DATABASE_URL: str = "postgres://{}:{}@{}:{}/{}".format(
    parameters["database"]["user"],
    parameters["database"]["password"],
    parameters["database"]["host"],
    parameters["database"]["port"],
    parameters["database"]["database"],
)


##
# API keys
##

ALPHA_VANTAGE_API_KEY: str = parameters["api-keys"]["alpha_vantage"]
