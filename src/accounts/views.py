import logging

from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponse, redirect, render
from django.views import View
from rest_framework import mixins, viewsets

from accounts.forms import UserLoginForm, UserRegisterForm
from accounts.models.custom_user import CustomUser
from accounts.serializers.custom_user_sr import UserSerializer
from profiles.models.profiles import Profile
from settings.sessions import FAILED_LOGIN_ATTEMPTS_LIMIT

logger = logging.getLogger(__name__)


def say_hi(request):
    logger.info("Visited say_hi view")
    return HttpResponse("<h1>Первые строчки проекта созданы</h1>")


class UserRegisterView(View):
    template_name = "register.html"

    def get(self, request):
        form = UserRegisterForm()
        logger.info("Rendering UserRegisterForm on GET request")
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            logger.info(f"User registered successfully: {user.username}")
            return redirect("login")
        else:
            logger.warning("User registration failed with errors")
            return render(request, self.template_name, {"form": form})


class UserLoginView(View):
    template_name = "login.html"
    failed_login_attempt_key = "failed_login_attempt_count"

    def get(self, request):
        form = UserLoginForm()
        logger.info("Rendering UserLoginForm on GET request")
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        request.session.setdefault(self.failed_login_attempt_key, 0)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                request.session[self.failed_login_attempt_key] = 0
                logger.info(f"User logged in successfully: {email}")
                return redirect("say_hi")
            else:
                request.session[self.failed_login_attempt_key] += 1
                error_msg = "Неправильно указали пароль или почту"
                form.add_error(None, error_msg)
                logger.warning(f"Failed login attempt for email: {email}")
        else:
            request.session[self.failed_login_attempt_key] += 1
            logger.warning("Form validation failed during login attempt")

        if (
            request.session[self.failed_login_attempt_key]
            >= FAILED_LOGIN_ATTEMPTS_LIMIT
        ):
            form.add_error(None, "Попробуйте зайти с помощью почты")

        return render(request, self.template_name, {"form": form})


# Аутентификация по коду из почты (пока не работает!)
"""
class VerificationView(View):
    def post(self, request):
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            verification_word = form.cleaned_data.get('verification_word')

            if verification_word == request.session.get('verification_code'):
                request.session['failed_login_attempts'] = 0
                user = CustomUser.objects.get(username=request.session.get('username'))
                login(request, user)
                logger.info(f"User verified and logged in: {user.username}")
                return redirect('say_hi')
            else:
                form.add_error(None, 'Неверный код.')
                logger.warning("Invalid verification code entered")
        return render(request, 'verification.html', {'form': form})
"""


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
