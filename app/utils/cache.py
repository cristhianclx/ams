# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Tuple

from fastapi import status
from redis import ConnectionPool, Redis
from settings import CACHE_URL, RATE_THROTTLING_PER_MINUTE, RATE_THROTTLING_PER_SECOND

CACHE_EXPIRY_TIME = 60 * 60


class CacheMixin:
    def _generate_key(self, api_key, identifier):
        return f"{self.CACHE_NAME}:{api_key}:{identifier}"


class BaseCache:
    def __init__(self):
        self.cache = Redis(connection_pool=ConnectionPool.from_url(CACHE_URL))

    def _get_value(self, key):
        return self.cache.get(key)

    def _set_value(self, key, value, timeout):
        self.cache.set(key, value, timeout)

    def _incr_value(self, key, amount=1, timeout=CACHE_EXPIRY_TIME):
        try:
            return self.cache.incr(key, amount)
        except ValueError:
            self._set_value(key, amount, timeout=timeout)
            return amount

    def _delete_value(self, key):
        self.cache.delete(key)

    def clear(self):
        self.cache.clear()


class MeteringCache(BaseCache, CacheMixin):

    CACHE_NAME = "metering"

    def _generate_usage_key_per_second(self, api_key):
        return self._generate_key(api_key, datetime.utcnow().strftime("%Y%m%d-%H%M%S"))

    def _generate_usage_key_per_minute(self, api_key):
        return self._generate_key(api_key, datetime.utcnow().strftime("%Y%m%d-%H%M"))

    def increment_api_usage(self, api_key):
        usage_per_second = self._incr_value(self._generate_usage_key_per_second(api_key))
        usage_per_minute = self._incr_value(self._generate_usage_key_per_minute(api_key))
        return {
            "per_second": usage_per_second,
            "per_minute": usage_per_minute,
        }

    def get_api_usage(self, api_key):
        usage_per_second = self._get_value(self._generate_usage_key_per_second(api_key))
        if not usage_per_second:
            usage_per_second = 0
        usage_per_minute = self._get_value(self._generate_usage_key_per_minute(api_key))
        if not usage_per_minute:
            usage_per_minute = 0
        return {
            "per_second": usage_per_second,
            "per_minute": usage_per_minute,
        }


def get_api_usage(current_user: User, token: str = Depends(get_current_active_user)) -> Tuple[User, dict]:
    usage = MeteringCache().get_api_usage(token)
    if usage["per_second"] >= RATE_THROTTLING_PER_SECOND:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Throttling per second")
    if usage["per_minute"] >= RATE_THROTTLING_PER_MINUTE:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Throttling per second")
    return current_user, MeteringCache().increment_api_usage(token)
