# Configurations for sending email, including SMTP server, sender settings and email templates.
import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_PORT = int(os.getenv("MAIL_SETTINGS_PORT"))
EMAIL_HOST = os.getenv("MAIL_SETTINGS_SERVER")
EMAIL_HOST_USER = os.getenv("MAIL_SETTINGS_EMAIL_ADDRESS")
EMAIL_HOST_PASSWORD = os.getenv("MAIL_SETTINGS_EMAIL_PASSWORD")
EMAIL_TIMEOUT = int(os.getenv("MAIL_SETTINGS_EMAIL_TIMEOUT"))
EMAIL_USE_TLS = bool(os.getenv("EMAIL_USE_TLS"))
# EMAIL_USE_SSL = bool(os.getenv('EMAIL_USE_SSL'))
