# -*- coding: utf-8 -*-

from datetime import datetime
from sys import path as sys__path

from models.stock import Stock

data = [
    {
        "code": "AAPL",
        "name": "Apple",
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1),
    },
    {
        "code": "AMZN",
        "name": "Amazon",
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1),
    },
    {
        "code": "GOOGL",
        "name": "Google",
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1),
    },
    {
        "code": "META",
        "name": "Faceboook",
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1),
    },
    {
        "code": "MSFT",
        "name": "Microsoft",
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1),
    },
]


sys__path.append("/code/")

from data.seed.base import load__data  # pylint: disable=import-error

load__data(Stock, Stock.code, data, "code")
