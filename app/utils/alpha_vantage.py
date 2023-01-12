# -*- coding: utf-8 -*-

from datetime import datetime
from json import dumps, loads

from fastapi import HTTPException, status
from requests import get
from settings import ALPHA_VANTAGE_API_KEY
from utils.cache import BaseCache, CacheMixin

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
CACHE_EXPIRY_TIME = 60 * 60 * 6


class AlphaVantageCache(BaseCache, CacheMixin):

    CACHE_NAME = "alpha-vantage"

    def _execute(self, code: str) -> dict:
        response = get(
            ALPHA_VANTAGE_URL,
            params={
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": f"{code}",
                "outputsize": "compact",
                "datatype": "json",
                "apikey": ALPHA_VANTAGE_API_KEY,
            },
            timeout=1,
        )
        if not response.ok:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not get data from service",
            )
        return response.json()

    def _generate_key_per_day(self, code: str) -> str:
        return self._generate_key(code, datetime.utcnow().strftime("%Y%m%d"))

    def get_data(self, code: str) -> dict:
        data = self._get_value(self._generate_key_per_day(code))
        if not data:
            data = self._execute(code)
            data = dumps(data)
            self._set_value(self._generate_key_per_day(code), data, CACHE_EXPIRY_TIME)
        data = loads(data)
        time_series_daily_0_key = list(data["Time Series (Daily)"].keys())[0]
        time_series_daily_0 = data["Time Series (Daily)"][time_series_daily_0_key]
        time_series_daily_1_key = list(data["Time Series (Daily)"].keys())[1]
        time_series_daily_1 = data["Time Series (Daily)"][time_series_daily_1_key]
        context = {
            "open": float(time_series_daily_0["1. open"]),
            "high": float(time_series_daily_0["2. high"]),
            "low": float(time_series_daily_0["3. low"]),
            "variation": round(float(time_series_daily_0["4. close"]) - float(time_series_daily_1["4. close"]), 2),
        }
        return context
