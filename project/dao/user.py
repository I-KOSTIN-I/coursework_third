from typing import Dict

from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def create(self, user_d: Dict):
        ent = User(**user_d)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent
