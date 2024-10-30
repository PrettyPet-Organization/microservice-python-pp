import logging
import smtplib
import ssl
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string

from settings import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    EMAIL_TIMEOUT,
    SMTP_PORT,
    SMTP_SERVER,
)


logger = logging.getLogger(__name__)


def create_and_send_email(send_to: str, template_name: str, context: dict, subject: str):
    """
    Creates the body of an email based on the context and template, and sends it using the configured SMTP server
    in the background to avoid blocking the calling code.
    :param send_to: recipient's email address
    :param template_name: full name of the template
    :param context: context for filling the template
    :param subject: subject of the email
    :return: None
    """

    def send_email_in_thread():
        try:
            email = _create_email(context, send_to, subject, template_name)
            _send_mail(email, send_to)
        except Exception as error:
            logger.error(f"Couldn't send email to {send_to=} with context {context=}, error occurred: {error}")

    email_thread = threading.Thread(target=send_email_in_thread)
    email_thread.start()


def _create_email(context: dict, send_to: str, subject: str, template_name: str) -> MIMEMultipart:
    """Creates an email for sending based on the provided text and template."""

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = send_to
    msg["Subject"] = subject

    html = render_to_string(template_name, context)

    content = MIMEText(html, "html", "UTF-8")
    msg.attach(content)
    return msg


def _send_mail(email: MIMEMultipart, send_to: str):
    """Sends the email using the SMTP server specified in the configuration."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=EMAIL_TIMEOUT) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, send_to, email.as_string())
