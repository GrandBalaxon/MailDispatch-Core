from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from core.forms import MailingRecipientForm, MailingForm, MessageForm
from core.mixins import UserQuerysetFilterMixin, OwnerOrManagerMixin, OwnerOnlyMixin
from core.models import Mailing, MailingRecipient, Message
from core.services import run_mailing


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        # Общее количество всех созданных рассылок
        total_mailings = Mailing.objects.all().count()
        context['total_mailings'] = total_mailings

        # Количество активных рассылок
        active_mailings = Mailing.objects.filter(status="launched").count()
        context['active_mailings'] = active_mailings

        # Количество уникальных получателей
        unique_receivers = MailingRecipient.objects.all().count()
        context['unique_receivers'] = unique_receivers

        return context


# model MailingRecipient views
class MailingRecipientsView(LoginRequiredMixin, UserQuerysetFilterMixin, ListView):
    model = MailingRecipient
    owner_field = 'added_by'
    template_name = "core/recipients/list.html"
    context_object_name = "recipients"


class RecipientDetailsView(OwnerOrManagerMixin, DetailView):
    model = MailingRecipient
    template_name = "core/recipients/details.html"
    owner_field = 'added_by'
    context_object_name = 'recipient'


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = "core/recipients/create.html"
    success_url = reverse_lazy("core:recipient_list")

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(OwnerOnlyMixin, UpdateView):
    model = MailingRecipient
    owner_field = 'added_by'
    form_class = MailingRecipientForm
    template_name = "core/recipients/update.html"
    success_url = reverse_lazy("core:recipient_list")


class RecipientDeleteView(OwnerOnlyMixin, DeleteView):
    model = MailingRecipient
    owner_field = 'added_by'
    template_name = "core/recipients/delete.html"
    success_url = reverse_lazy("core:recipient_list")
    context_object_name = "recipient"


# model Mailing views
class MailingsView(LoginRequiredMixin, UserQuerysetFilterMixin, ListView):
    model = Mailing
    template_name = "core/mailings/list.html"
    context_object_name = "mailings"


class MailingDetailsView(OwnerOrManagerMixin, DetailView):
    model = Mailing
    template_name = "core/mailings/details.html"
    owner_field = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.object
        mailing.update_status()
        context['mailing'] = mailing
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "core/mailings/create.html"
    success_url = reverse_lazy("core:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MailingUpdateView(OwnerOnlyMixin, UpdateView):
    model = Mailing
    owner_field = 'author'
    form_class = MailingForm
    template_name = "core/mailings/update.html"
    success_url = reverse_lazy("core:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDeleteView(OwnerOnlyMixin, DeleteView):
    model = Mailing
    owner_field = 'author'
    template_name = "core/mailings/delete.html"
    success_url = reverse_lazy("core:mailing_list")
    context_object_name = "mailing"


@login_required
def mailing_run_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if request.user != mailing.author:
        return HttpResponseForbidden("Только владелец может запускать рассылку.")

    try:
        run_mailing(mailing)
        messages.success(request, "Рассылка успешно выполнена!")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('core:mailing_details', pk=pk)


# model Messages views
class MessagesView(LoginRequiredMixin, UserQuerysetFilterMixin, ListView):
    model = Message
    template_name = "core/messages/list.html"
    context_object_name = "messages"


class MessageDetailsView(OwnerOrManagerMixin, DetailView):
    model = Message
    template_name = "core/messages/details.html"
    owner_field = 'author'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "core/messages/create.html"
    success_url = reverse_lazy("core:message_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MessageUpdateView(OwnerOnlyMixin, UpdateView):
    model = Message
    owner_field = 'author'
    form_class = MessageForm
    template_name = "core/messages/update.html"
    success_url = reverse_lazy("core:message_list")


class MessageDeleteView(OwnerOnlyMixin, DeleteView):
    model = Message
    owner_field = 'author'
    template_name = "core/messages/delete.html"
    success_url = reverse_lazy("core:message_list")
    context_object_name = "message"
