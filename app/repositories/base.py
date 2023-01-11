# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, reference):
        raise NotImplementedError
