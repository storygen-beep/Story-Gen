"""
Authentication URL patterns matching FastAPI routes exactly.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Authentication endpoints - match FastAPI exactly (no trailing slash)
    path("register", views.RegisterView.as_view(), name="auth_register"),
    path("login", views.LoginView.as_view(), name="auth_login"),
    path("refresh", views.RefreshTokenView.as_view(), name="auth_refresh"),
    path("verify-token", views.VerifyTokenView.as_view(), name="auth_verify_token"),
    path("me", views.MeView.as_view(), name="auth_me"),
    # Additional endpoints
    path("change-password", views.ChangePasswordView.as_view(), name="change_password"),
]
