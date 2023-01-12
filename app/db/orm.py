# -*- coding: utf-8 -*-

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class ModelBase(Base):
    __abstract__: bool = True

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


from models import *  # noqa:E402,F401,F403 # pylint:disable=wildcard-import,wrong-import-position,unused-wildcard-import
