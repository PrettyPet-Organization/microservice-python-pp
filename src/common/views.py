import logging
from datetime import datetime
from random import choice

import pycountry
import pytz
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


# Creating a logger
logger = logging.getLogger(__name__)


class RandomTimeView(APIView):
    """
    A representation function that returns a random country
    and its time in the format '%H:%M:%S'
    results as a JSON response.

    :param request: The rest_framework Request object.
    :type request: Request

    :return: random country and time
    :rtype: Response
    """

    def get(self, request: Request) -> Response:
        logger.info("Request to get a random country and time in it.")
        random_country = choice(list(pycountry.countries))
        country_name = _(random_country.name)
        tz_name = pytz.timezone(pytz.country_timezones.get(random_country.alpha_2, [])[0])
        current_time = datetime.now(tz_name)
        logger.info(f"Now in {country_name}: {current_time.strftime('%H:%M:%S')}")

        return Response({"country": country_name, "time": current_time.strftime("%H:%M:%S")})
