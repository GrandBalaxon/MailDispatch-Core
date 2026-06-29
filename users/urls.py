from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.views import *

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("login/",LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset/email_form.html',
             email_template_name='users/password_reset/email.html',
             success_url=reverse_lazy('users:password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset/mail_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset/confirm.html',
             success_url=reverse_lazy('users:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset/complete.html'),
         name='password_reset_complete'),
]