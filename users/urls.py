from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from core.mixins import StyleFormMixin
from users.views import *

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("login/",LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
]