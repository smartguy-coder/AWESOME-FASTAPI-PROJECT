import os
from pathlib import Path

from app.utils.email.custom_solution import email_custom_utils
from app.settings import settings


def send_email_verification(user_email: str, user_uuid: str, user_name: str, host: str = 'http://127.0.0.1:8000'):
    activate_url = f'{host}api/users/verify/{user_uuid}'
    # os.path.join(os.path.dirname(file), 'real_tracking_nova_post.json
    with open((Path(__file__).parent.parent / 'templates' / 'user' / 'account-verification.html'), encoding='utf-8') as file:
        content = file.read()
        content = content.replace(
            '{{ app_name }}', settings.APP_NAME,
        ).replace(
            '{{ name }}', user_name,
        ).replace(
            '{{ activate_url }}', activate_url,
        )
    email_custom_utils.send_email(
        recipients=[user_email], mail_body=content, mail_subject=f'Account Verification - {settings.APP_NAME}',
    )
