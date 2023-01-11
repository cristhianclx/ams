# -*- coding: utf-8 -*-

from typing import List

from forms.user import UserForm
from repositories.user import UserRepository
from db.engine import SessionLocal


class UserService:

    def __init__(self) -> None:
        self.repository = UserRepository
        self.schema = UserForm

    def create(
        self,
        db: SessionLocal,
        item: UserForm,
    ) -> UserForm:
        repo = self.repository(db)
        cc = repo.create(item=item)
        return self.schema.from_orm(cc)

    def get(
        self,
        db: SessionLocal,
        email: str,
    ) -> UserForm:
        repo = self.repository(db)
        return repo.get(email=email)

    def update(
        self,
        db: SessionLocal,
        email: str,
        item: UserForm,
    ) -> UserForm:
        repo = self.repository(db)
        return repo.update(reference=reference, item=item)
