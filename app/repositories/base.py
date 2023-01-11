# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    def get(self, reference):
        raise NotImplementedError
