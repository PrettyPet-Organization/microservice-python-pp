from django.urls import path
from rest_framework.routers import DefaultRouter

from projects import views


router = DefaultRouter()
router.register(r"all", views.ProjectViewSet)

urlpatterns = [
    path(
        "overview/",
        views.ProjectsOverviewView.as_view(),
        name="projects_overview",
    )
]

urlpatterns += router.urls
