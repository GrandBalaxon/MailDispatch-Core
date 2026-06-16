from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from core.forms import MailingRecipientForm, MailingForm, MessageForm
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
class MailingRecipientsView(ListView):
    model = MailingRecipient
    template_name = "core/recipients/list.html"
    context_object_name = "recipients"


class RecipientDetailsView(TemplateView):
    model = MailingRecipient
    template_name = "core/recipients/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipient = MailingRecipient.objects.get(pk=self.kwargs["pk"])
        context['recipient'] = recipient
        return context


class RecipientCreateView(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = "core/recipients/create.html"
    success_url = reverse_lazy("core:recipient_list")


class RecipientUpdateView(UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = "core/recipients/update.html"
    success_url = reverse_lazy("core:recipient_list")


class RecipientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = "core/recipients/delete.html"
    success_url = reverse_lazy("core:recipient_list")
    context_object_name = "recipient"


# model Mailing views
class MailingsView(ListView):
    model = Mailing
    template_name = "core/mailings/list.html"
    context_object_name = "mailings"


class MailingDetailsView(TemplateView):
    model = Mailing
    template_name = "core/mailings/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = Mailing.objects.get(pk=self.kwargs["pk"])
        mailing.update_status()
        context['mailing'] = mailing
        return context


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "core/mailings/create.html"
    success_url = reverse_lazy("core:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "core/mailings/update.html"
    success_url = reverse_lazy("core:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "core/mailings/delete.html"
    success_url = reverse_lazy("core:mailing_list")


# model Messages views
class MessagesView(ListView):
    model = Message
    template_name = "core/messages/list.html"
    context_object_name = "messages"


class MessageDetailsView(TemplateView):
    model = Message
    template_name = "core/messages/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = Message.objects.get(pk=self.kwargs["pk"])
        context['message'] = message
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "core/messages/create.html"
    success_url = reverse_lazy("core:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "core/messages/update.html"
    success_url = reverse_lazy("core:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "core/messages/delete.html"
    success_url = reverse_lazy("core:message_list")


def mailing_run_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    run_mailing(mailing)
    return redirect('core:mailing_details', pk=pk)
