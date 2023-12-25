from pathlib import Path

from app.settings import settings
from app.utils.email.custom_solution import email_custom_utils


def send_email_verification(user_email: str, user_uuid: str, user_name: str, host: str = "http://127.0.0.1:8000"):
    activate_url = f"{host}api/users/verify/{user_uuid}"
    with open(
        (Path(__file__).parent.parent / "templates" / "user" / "account-verification.html"), encoding="utf-8"
    ) as file:
        content = file.read()
        content = (
            content.replace("{{ app_name }}", settings.APP_NAME)
            .replace("{{ name }}", user_name)
            .replace("{{ activate_url }}", activate_url)
        )
    email_custom_utils.send_email(
        recipients=[user_email],
        mail_body=content,
        mail_subject=f"Account Verification - {settings.APP_NAME}",
    )


def send_email_forgot_password_link(
    user_email: str, user_uuid: str, user_name: str, host: str = "http://127.0.0.1:8000"
):
    activate_url = f"{host}api/auth/reset-password/{user_uuid}"

    with open((Path(__file__).parent.parent / "templates" / "auth" / "password-reset.html"), encoding="utf-8") as file:
        content = file.read()
        content = (
            content.replace("{{ app_name }}", settings.APP_NAME)
            .replace("{{ name }}", user_name)
            .replace("{{ activate_url }}", activate_url)
        )
    email_custom_utils.send_email(
        recipients=[user_email],
        mail_body=content,
        mail_subject=f"Reset password - {settings.APP_NAME}",
    )
