import base64
import os

import pyotp


class OneTimePassword:
    TOKEN_LENGTH = 6

    @staticmethod
    async def verify_otp(secret, otp):
        totp = pyotp.TOTP(secret)
        return totp.verify(otp)

    @staticmethod
    def create_otp_secret() -> str:
        return base64.b32encode(os.urandom(20)).decode("utf-8")
