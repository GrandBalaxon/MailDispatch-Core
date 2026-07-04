from secrets import token_hex

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, RedirectView

from config.settings import EMAIL_HOST_USER
from core.models import Mailing, MailingRecipient, MailingAttempt
from users.forms import CustomUserCreationForm
from users.models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения почты перейдите по следующей ссылке - {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return render(request, 'users/email_confirmed.html')


class UserProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def test_func(self):
        """Обычный пользователь может смотреть только свой профиль, менеджер — любой."""
        profile_user = self.get_object()
        request_user = self.request.user
        if request_user.role == 'manager':
            return True
        return profile_user == request_user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("У вас нет прав для просмотра этого профиля.")
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object

        # Статистика
        context['total_mailings'] = Mailing.objects.filter(author=profile_user).count()
        context['active_mailings'] = Mailing.objects.filter(
            author=profile_user, status='launched'
        ).count()
        context['total_recipients'] = MailingRecipient.objects.filter(
            added_by=profile_user
        ).count()
        context['total_attempts'] = MailingAttempt.objects.filter(
            mailing__author=profile_user
        ).count()

        # Последние рассылки и получатели
        context['recent_mailings'] = Mailing.objects.filter(
            author=profile_user
        ).order_by('-start_time')[:5]

        context['recent_recipients'] = MailingRecipient.objects.filter(
            added_by=profile_user
        ).order_by('-id')[:5]

        return context
