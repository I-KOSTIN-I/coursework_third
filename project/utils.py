import json
import hashlib
from project import config
import base64


def read_json(filename, encoding="utf-8"):
    with open(filename, encoding=encoding) as f:
        return json.load(f)


def get_hash(password: str) -> str:
    hash_pass = hashlib.pbkdf2_hmac(
        hash_name=config.PWD_HASH_NAME,
        salt=config.PWD_HASH_SALT.encode('utf-8'),
        iterations=config.PWD_HASH_ITERATIONS,
        password=password.encode('utf-8')
    )

    return base64.b64encode(hash_pass).decode('utf-8')