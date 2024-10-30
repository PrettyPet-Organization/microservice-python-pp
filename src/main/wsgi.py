"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import logging.config
import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application


logging_conf = settings.LOGGING
logging.config.dictConfig(logging_conf)
logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

application = get_wsgi_application()
logger.info("The project on the WSGI server has been successfully launched")
