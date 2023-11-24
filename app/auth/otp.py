import pyotp, base64, qrcode, uuid

from dao import get_user_by_id, get_user_login_by_id


def get_encoded_user_uuid(secret: str) -> bytes:
    key_in_bytes = bytes(secret, 'utf-8')
    encoded_user_uuid = base64.b32encode(key_in_bytes)
    return encoded_user_uuid

#
# async def get_changed_login(login: str):
#     changed_login = login.replace('@', '_')
#     return changed_login
#
#
# async def get_qr_code_path_by_changed_login(changed_login):
#     path = f'app/templates/qr_images/qrcode_{changed_login}.png'
#
#
# async def get_otp_name(changed_login: str) -> str:
#     otp_name = f'FastAPI Project ({changed_login})'


async def create_qr(user_uuid_str, user_id):
    secret = bytes(user_uuid_str, 'utf-8')
    otp_key = base64.b32encode(secret)
    otp_name = f'Fast api project'
    uri = pyotp.totp.TOTP(otp_key).provisioning_uri(name=otp_name)
    qrcode.make(uri).save(f'app/templates/qr_images/qrcode_{user_id}.png')


async def verify_otp(otp_password_input, user_uuid_str):
    secret = bytes(user_uuid_str, 'utf-8')
    otp_key = base64.b32encode(secret)
    totp = pyotp.TOTP(otp_key)
    return totp.verify(otp_password_input)
