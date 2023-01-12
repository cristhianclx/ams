# -*- coding: utf-8 -*-

from db.engine import SessionLocal
from forms.user import UserForm
from models.user import User
from repositories.user import UserRepository


class UserService:
    def __init__(self) -> None:
        self.repository = UserRepository

    def create(
        self,
        session: SessionLocal,
        item: UserForm,
    ) -> User:
        repo = self.repository(session)
        return repo.create(item=item)

    def get(
        self,
        session: SessionLocal,
        email: str,
    ) -> User:
        repo = self.repository(session)
        return repo.get(reference=email)
