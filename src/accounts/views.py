import datetime
import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts import messages
from accounts.serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer
from settings import FAILED_LOGIN_ATTEMPTS_LIMIT
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from celery import shared_task

# Creating a logger
logger = logging.getLogger(__name__)


class UserRegisterView(APIView):
    """
    Handles user registration.

    Inherits from `APIView` and manages user creation by handling POST requests
    with user registration data. Upon successful registration, a 201 (Created)
    status is returned. If the request contains invalid data, a 400 (Bad Request)
    status is returned with validation errors.

    Methods:
        post(request):
            Handles user registration by validating the input data with
            `UserRegisterSerializer`. Returns HTTP 201 if successful or
            HTTP 400 in case of validation failure.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        """
        Processes a POST request to register a new user.

        Args:
            request (Request): The HTTP request object containing user registration data.

        Returns:
            Response:
                - HTTP 201 (Created) if the user is successfully registered.
                - HTTP 400 (Bad Request) if the input data fails validation.
        """
        logger.info("Received registration request: %s", request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("User successfully registered.")
            return Response(status=status.HTTP_201_CREATED)

        logger.warning("User registration failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle obtaining a new JWT token pair.

    Inherits from `TokenObtainPairView` and logs attempts to obtain new access
    and refresh tokens. If authentication is successful, logs the username;
    if it fails, logs the request data causing failure.

    Methods:
        post(request, *args, **kwargs):
            Processes a POST request to obtain a new token pair. Logs both
            successful and failed attempts.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Processes a POST request to obtain a new JWT token pair.

        Args:
            request (Request): The HTTP request object containing user login data.

        Returns:
            Response: HTTP 200 if authentication is successful, otherwise appropriate error status.
        """
        logger.info("Authentication attempt with data: %s", request.data)
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            logger.info(f"User successfully authenticated.")
        else:
            logger.warning(f"Failed authentication attempt with data: {request.data}.")

        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to handle refreshing JWT tokens.

    Inherits from `TokenRefreshView` and logs token refresh attempts.
    Logs a successful token refresh or failure details.

    Methods:
        post(request, *args, **kwargs):
            Processes a POST request to refresh a JWT token.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Processes a POST request to refresh a JWT token.

        Args:
            request (Request): The HTTP request object containing the refresh token.

        Returns:
            Response: HTTP 200 if the token is successfully refreshed, otherwise appropriate error status.
        """
        logger.info("Token refresh attempt with data: %s", request.data)
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            logger.info("Token successfully refreshed.")
        else:
            logger.warning(f"Token refresh failed with response: {response.data}.")

        return response


class CustomTokenBlacklistView(TokenBlacklistView):
    """
    Custom view to handle blacklisting JWT tokens during logout.

    Inherits from `TokenBlacklistView` and logs token blacklisting attempts.
    Logs a successful logout or failure details.

    Methods:
        post(request, *args, **kwargs):
            Processes a POST request to blacklist the token during logout.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Processes a POST request to blacklist a JWT token during logout.

        Args:
            request (Request): The HTTP request object containing the token to blacklist.

        Returns:
            Response: HTTP 200 if the token is successfully blacklisted, otherwise appropriate error status.
        """
        logger.info("Logout attempt with data: %s", request.data)
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            logger.info("Logout successful, token added to blacklist.")
        else:
            logger.warning(f"Logout failed with response: {response.data}.")

        return response


@shared_task
def send_email_survey_about_the_platform():

    try:
        users = User.objects.all()
        for user in users:
            subject = "Опрос о платформе Pretty Pet"
            time_difference = datetime.datetime.now() - user.customuser.date_joined
            if time_difference >= datetime.timedelta(hours=24):
                if user.customuser.confirmed_form_about_platform: #We check whether the user has sent a request
                    message = (
                        "Привет, {}!\n\n"
                        "Спасибо, что присоединился к нашей платформе! "
                        "Поделись своим первым впечатлением, ответив на пару вопросов: "
                        "[Ссылка на анкету]"
                    ).format(user.customuser.username)
                    user.customuser.confirmed_form_about_platform == True
                    user.customuser.save()
                else:
                    message = (
                        "Привет, {}!\n\n"
                        "Приглашаем тебя подать заявку на участие в нашей платформе! "
                        "Это займет всего несколько минут: [Ссылка на заявку]"
                    ).format(user.customuser.username)

                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.customuser.email]
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=False,
                )

        return status.HTTP_200_OK
    except Exception as er:
        return status.HTTP_400_BAD_REQUEST


class EmailAPIView(APIView):
    """
    Processes a POST request to email send.

    Args:
        request (Request): The HTTP request start email send.

    Returns:
        Response: HTTP 200 if send email.
    """
    def post(self, request):
        email_send = send_email_survey_about_the_platform.delay()
        if email_send == status.HTTP_200_OK:
            return Response({"status": "success", "message": f"Ok. {status.HTTP_200_OK}"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message": f"Error: {status.HTTP_400_BAD_REQUEST}"},
                            status=status.HTTP_400_BAD_REQUEST)


