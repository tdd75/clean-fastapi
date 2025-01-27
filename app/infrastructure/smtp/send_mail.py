import logging
from typing import Iterable, TypedDict, NotRequired
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from app import setting

logger = logging.getLogger(__name__)


class Mail(TypedDict):
    receivers: list[str]
    subject: str
    text_content: NotRequired[str]
    html_content: NotRequired[str]
    attachment_paths: NotRequired[list[str]]


def send_mail(mail_list: Iterable[Mail]) -> None:
    if not setting.SMTP_USER or not setting.SMTP_PASSWORD:
        logger.info('SMTP is not configured')
        return

    server = smtplib.SMTP(setting.SMTP_HOST, setting.SMTP_PORT)

    if setting.SMTP_TLS:
        server.starttls()
        server.login(setting.SMTP_USER, setting.SMTP_PASSWORD)

    for email in mail_list:
        message = MIMEMultipart()
        message['From'] = setting.SMTP_USER
        message['To'] = ', '.join(email['receivers'])
        message['Subject'] = email['subject']
        if 'text_content' in email:
            message.attach(MIMEText(email['text_content']))
        if 'html_content' in email:
            message.attach(MIMEText(email['html_content'], 'html'))

        if 'attachment_paths' in email:
            for attachment_path in email['attachment_paths']:
                with open(attachment_path, 'rb') as attachment:
                    att = MIMEApplication(attachment.read())
                    att.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=str(attachment_path.split('/')[-1]),
                    )
                    message.attach(att)
        text = message.as_string()

        server.sendmail(setting.SMTP_USER, email['receivers'], text)
    server.quit()
