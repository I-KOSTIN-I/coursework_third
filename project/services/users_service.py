from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.utils import get_hash


class UsersService(BaseService):

    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def create(self, user_d):
        user_d['password'] = get_hash(user_d['password'])
        return UserDAO(self._db_session).create(user_d)

    def update(self, user_d):
        if user_d.get('password') is not None:
            user_d['password'] = get_hash(user_d['password'])
        return UserDAO(self._db_session).update(user_d)

    def change_password(self, user_d):
        new_password = user_d.get('new_password')
        old_password = user_d.get('old_password')
        old_password_hash = get_hash(old_password)
        user = UserDAO(self._db_session).get_by_id(user_d['id'])
        password_db = user.password

        if old_password_hash == password_db:
            user_d['password'] = get_hash(new_password)
            user_update = UserDAO(self._db_session).update(user_d)

            return user_update, print("password changed")

        return print("the old password is incorrect")
