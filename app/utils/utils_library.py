import base64
import random
import secrets
import string
import uuid


def create_str_uuid4() -> str:
    result = str(uuid.uuid4())
    return result


def make_randon_assii_string(length: int = 5) -> str:
    """no spaces"""
    ascii_chars = string.digits + string.ascii_letters + string.punctuation
    return "".join(random.choices(ascii_chars, k=length))


def unique_string(byte: int = 8) -> str:
    return secrets.token_urlsafe(byte)


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode("ascii")).decode("ascii")


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode("ascii")).decode("ascii")
