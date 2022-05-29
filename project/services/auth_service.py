
from flask_restx import abort
from sqlalchemy.orm import scoped_session

from project.dao import AuthDAO
from project.services.base import BaseService
from project.utils import get_hash, generate_tokens, decode_token


class AuthService(BaseService):

    def __init__(self, session: scoped_session):
        super().__init__(session)

    def login(self, user_d: dict):
        user_data = AuthDAO(self._db_session).get_by_email(user_d['email'])
        print(user_data)
        if user_data.email is None:
            abort(401, message='user not found')

        hashed_pass = get_hash(user_d['password'])
        if user_data.password != hashed_pass:
            abort(401, message='invalid credentials')

        tokens = generate_tokens(
            {
                'email': user_d['email'],
                'password': user_d['password']
            }
        )

        return tokens

    def get_new_tokens(self, refresh_token: str):

        decoded_token = decode_token(refresh_token, refresh_token=True)

        tokens = generate_tokens(
            user_d={
                'email': decoded_token['email'],
            }
        )

        return tokens
