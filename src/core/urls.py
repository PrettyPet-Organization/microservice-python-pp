from django.urls import path

from core.views.check_system import CheckSystem


urlpatterns = [
    path("check-logs/", CheckSystem.as_view(), name="check_logs"),
]
