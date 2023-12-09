import uuid as uuid_pkg


def create_str_uuid4() -> str:
    result = str(uuid_pkg.uuid4())
    return result
