# -*- coding: utf-8 -*-

from typing import List

from db.engine import SessionLocal as Session
from db.orm import Base


def load__data(Model: Base, ModelReference: any, data: List, reference):
    session = Session()
    IDs = [d[reference] for d in data]
    items__in = session.query(Model).filter(ModelReference.in_(IDs)).all()
    items__in__IDs = [i.__dict__[reference] for i in items__in]
    items = [Model(**d) for d in data if d[reference] not in items__in__IDs]
    session.add_all(items)
    session.commit()
