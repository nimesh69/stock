# accounts/urls.py

from django.urls import path
from .views import (
    CsrfTokenView,
    LoginView,
    LogoutView,
    MeView,
    SignUpView,
)

urlpatterns = [
    path("csrf/", CsrfTokenView.as_view(), name="csrf"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
]