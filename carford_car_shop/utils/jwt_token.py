import jwt
import os
from dotenv import load_dotenv, find_dotenv


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

JWT_SECRET = os.environ.get("JWT_SECRET")


def jwt_encode(payload_data):
    """Encode data to a jwt token"""
    return jwt.encode(payload=payload_data, key=JWT_SECRET)


def jwt_decode(token):
    """Try to decode a token and validate it"""
    try:
        header_data = jwt.get_unverified_header(token)

        return jwt.decode(token, key=JWT_SECRET, algorithms=[header_data["alg"]])
    except jwt.exceptions.DecodeError:
        return False
