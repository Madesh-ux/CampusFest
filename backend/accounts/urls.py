from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            next_page="accounts:dashboard",
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="home"),
        name="logout",
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
]
