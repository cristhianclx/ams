# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, reference: Any) -> Any:
        raise NotImplementedError
