from project.dao.models.user import User
from project.utils import get_hash


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create(self, user_d: dict):
        user_d['password'] = get_hash(user_d['password'])
        return self.create(user_d)

    def get_by_username(self, user_d):
        result = self.session.query(User).filter(User.name == user_d).first()
        return result
