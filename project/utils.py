import json
import hashlib
from project.config import BaseConfig
from flask_restx import abort
from datetime import datetime, timedelta
import jwt
from flask import request, current_app
from typing import Dict


def read_json(filename, encoding="utf-8"):
    with open(filename, encoding=encoding) as f:
        return json.load(f)


def get_hash(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.BaseConfig.PWD_HASH_SALT,
        iterations=current_app.BaseConfig.PWD_HASH_ITERATIONS,
    )


def generate_tokens(user_d: dict) -> Dict[str, str]:
    user_d['exp'] = datetime.utcnow() + timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
    user_d['refresh_token'] = False

    access_token = jwt.encode(
        payload=user_d,
        key=BaseConfig.SECRET_KEY,
        algorithm=BaseConfig.JWT_ALGORITHM
    )

    user_d['exp'] = datetime.utcnow() + timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
    user_d['refresh_token'] = True

    refresh_token = jwt.encode(
        payload=user_d,
        key=BaseConfig.SECRET_KEY,
        algorithm=BaseConfig.JWT_ALGORITHM
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def get_token_from_headers(headers: dict):
    if 'Authorization' not in headers:
        abort(401)

    return headers['Authorization'].split(' ')[-1]


def decode_token(token: str, refresh_token: bool = False):

    decoded_token = {}

    try:
        decoded_token = jwt.decode(
            payload=token,
            key=BaseConfig.SECRET_KEY,
            algorithm=BaseConfig.JWT_ALGORITHM
        )
    except jwt.PyJWTError as e:
        current_app.logger.info('Got wrong token: "%s"', token)
        abort(401)

    if decoded_token['refresh_token'] != refresh_token:
        abort(400, message='Got wrong token type')

    return decoded_token


def auth_required(func):
    def wrapper(*args, **kwargs):

        token = get_token_from_headers(request.headers)

        decoded_token = decode_token(token)

        if not decoded_token['name']:
            abort(401)

        return func(*args, **kwargs)
    return wrapper


def admin_access_required(func):
    def wrapper(*args, **kwargs):

        token = get_token_from_headers(request.headers)

        decoded_token = decode_token(token)

        if decoded_token['role'] != 'admin':
            abort(403)

        if not decoded_token['name']:
            abort(401)

        return func(*args, **kwargs)
    return wrapper





