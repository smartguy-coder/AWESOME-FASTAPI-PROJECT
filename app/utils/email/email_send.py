import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


def email_sender(
        recipient: str,
        data_to_send: str,
        subject: str
):
    server = os.getenv('SMTP_SERVER')
    password = os.getenv('TOKEN_API')
    user = os.getenv('USER')

    msg = MIMEMultipart('alternative')
    if subject == 'Varify':
        @lru_cache
        def data_from_file(file):
            with open(file) as file:
                content = file.read()
                edited = content.format(name=recipient, subject=subject, code=data_to_send)
            return edited

        msg['Subject'] = subject
        text_to_send = MIMEText(data_from_file(file='email_templates/email_varify.html'), 'html')
        msg.attach(text_to_send)

    else:
        @lru_cache
        def data_from_file(file):
            with open(file) as file:
                content = file.read()
                edited = content.format(data=data_to_send)
            return edited

        msg['Subject'] = subject
        text_to_send = MIMEText(data_from_file(file='email_templates/email_page.html'), 'html')
        msg.attach(text_to_send)
    msg['From'] = f'From <{user}>'
    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(user, recipient, msg.as_string())
    mail.quit()
