from secrets import token_hex

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, TemplateView

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


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Статистика
        context['total_mailings'] = Mailing.objects.filter(author=user).count()
        context['active_mailings'] = Mailing.objects.filter(
            author=user, status='launched'
        ).count()
        context['total_recipients'] = MailingRecipient.objects.filter(
            added_by=user
        ).count()
        context['total_attempts'] = MailingAttempt.objects.filter(
            mailing__author=user
        ).count()

        # Последние рассылки и получатели
        context['recent_mailings'] = Mailing.objects.filter(
            author=user
        ).order_by('-start_time')[:5]

        context['recent_recipients'] = MailingRecipient.objects.filter(
            added_by=user
        ).order_by('-id')[:5]

        return context