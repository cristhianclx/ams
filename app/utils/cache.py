# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Tuple

from fastapi import Depends, HTTPException, status
from models.user import User
from redis import ConnectionPool, StrictRedis
from settings import CACHE_URL, RATE_THROTTLING_PER_MINUTE, RATE_THROTTLING_PER_SECOND
from utils.auth import get_current_active_user

CACHE_EXPIRY_TIME = 60 * 60


class CacheMixin:
    def _generate_key(self, api_key: str, identifier: str) -> str:
        return f"{self.CACHE_NAME}:{api_key}:{identifier}"  # type: ignore [attr-defined]


class BaseCache:
    def __init__(self) -> None:
        self.cache = StrictRedis(
            connection_pool=ConnectionPool.from_url(CACHE_URL), charset="utf-8", decode_responses=True
        )

    def _get_value(self, key: str) -> Any:
        return self.cache.get(key)

    def _set_value(self, key: str, value: Any, timeout: int) -> None:
        self.cache.set(key, value, timeout)

    def _incr_value(self, key: str, amount: int = 1, timeout: int = CACHE_EXPIRY_TIME) -> Any:
        try:
            return self.cache.incr(key, amount)
        except ValueError:
            self._set_value(key, amount, timeout=timeout)
            return amount

    def _delete_value(self, key: str) -> None:
        self.cache.delete(key)

    def clear(self) -> None:
        self.cache.delete(*self.cache.keys("*"))


class MeteringCache(BaseCache, CacheMixin):

    CACHE_NAME = "metering"

    def _generate_usage_key_per_second(self, api_key: str) -> str:
        return self._generate_key(api_key, datetime.utcnow().strftime("%Y%m%d-%H%M%S"))

    def _generate_usage_key_per_minute(self, api_key: str) -> str:
        return self._generate_key(api_key, datetime.utcnow().strftime("%Y%m%d-%H%M"))

    def increment_api_usage(self, api_key: str) -> dict:
        usage_per_second = self._incr_value(self._generate_usage_key_per_second(api_key))
        usage_per_minute = self._incr_value(self._generate_usage_key_per_minute(api_key))
        return {
            "per_second": usage_per_second,
            "per_minute": usage_per_minute,
        }

    def get_api_usage(self, api_key: str) -> dict:
        usage_per_second = int(self._get_value(self._generate_usage_key_per_second(api_key)) or 0)
        usage_per_minute = int(self._get_value(self._generate_usage_key_per_minute(api_key)) or 0)
        return {
            "per_second": usage_per_second,
            "per_minute": usage_per_minute,
        }


def get_api_usage(current_user_with_token: Tuple[User, str] = Depends(get_current_active_user)) -> Tuple[User, dict]:
    current_user, token = current_user_with_token
    usage = MeteringCache().get_api_usage(token)
    if usage["per_second"] >= RATE_THROTTLING_PER_SECOND:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Throttling per second")
    if usage["per_minute"] >= RATE_THROTTLING_PER_MINUTE:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Throttling per minute")
    return current_user, MeteringCache().increment_api_usage(token)
