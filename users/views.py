from secrets import token_hex

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from core.models import Mailing, MailingRecipient, MailingAttempt
from users.forms import CustomUserCreationForm, CustomUserUpdateForm
from users.models import CustomUser


class UsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'users/list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.role == 'manager'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("У вас нет прав для посещения данного раздела.")
        return super().handle_no_permission()


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


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/profile_edit.html'

    def test_func(self):
        profile_user = self.get_object()
        return profile_user == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("Только владелец может редактировать свой профиль.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.object.pk})


@require_POST
@login_required
def toggle_user_active(request, pk):
    if request.user.role != 'manager':
        return HttpResponseForbidden("Только менеджер может блокировать пользователей.")

    user = get_object_or_404(CustomUser, pk=pk)

    if user == request.user:
        return HttpResponseForbidden("Нельзя заблокировать самого себя.")

    user.is_active = not user.is_active
    user.save()
    return redirect('users:profile', pk=user.pk)
