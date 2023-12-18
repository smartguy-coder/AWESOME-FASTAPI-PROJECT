import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from app.settings import settings


def send_email(
    *,
    recipients: list[str],
    mail_body: str,
    mail_subject: str,
    attachment: str = None,
    mime_type: str = 'html',
):
    SERVER = settings.SMTP_SERVER
    PASSWORD = settings.EMAIL_TOKEN
    USER = settings.EMAIL_USER

    msg = MIMEMultipart('alternative')
    msg['Subject'] = mail_subject
    msg['From'] = f'<{settings.APP_NAME} {USER}>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = USER
    msg['Return-Path'] = USER
    msg['X-Mailer'] = 'decorator'

    if attachment:
        file_exists = os.path.exists(attachment)
        if not file_exists:
            print(f"file {attachment} does not exist")
        else:
            basename = os.path.basename(attachment)
            filesize = os.path.getsize(attachment)
            file = MIMEBase('application', f'octet-stream; name={basename}')
            file.set_payload(open(attachment, 'rb').read())
            file.add_header('Content-Description', attachment)
            file.add_header('Content-Description', f'attachment; filename={attachment}; size={filesize}')
            encoders.encode_base64(file)
            msg.attach(file)

    text_to_send = MIMEText(mail_body, mime_type)  # plain, html, image, audio, video https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
    msg.attach(text_to_send)

    mail = smtplib.SMTP_SSL(SERVER)
    mail.login(USER, PASSWORD)
    mail.sendmail(USER, recipients, msg.as_string())
    mail.quit()
