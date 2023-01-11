# -*- coding: utf-8 -*-

from db.engine import SessionLocal


def get__database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
