from django.urls import path

from accounts import views


urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", views.CustomTokenRefreshView.as_view(), name="refresh"),
    path("logout/", views.CustomTokenBlacklistView.as_view(), name="logout"),
    path("email/", views.EmailAPIView.as_view(), name="email"),
    # path('verify/', views.VerificationView.as_view(), name='verify'),
]
