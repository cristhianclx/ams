# -*- coding: utf-8 -*-


from db.engine import SessionLocal
from forms.user import UserForm
from models.user import User
from repositories.base import AbstractRepository


class UserRepository(AbstractRepository):
    def __init__(self, session: SessionLocal):
        self.model = User
        self.session = session

    def create(self, item: UserForm) -> User:
        values = item.dict()
        item = self.model(**values)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get(self, email: str) -> User:
        return (
            self.session.query(self.model)
            .filter(
                self.model.email == email,
            )
            .first()
        )
