from django.db.models import Prefetch, Count, OuterRef, Subquery
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from core.forms import MailingRecipientForm, MailingForm
from core.models import Mailing, MailingRecipient, Message


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


class RecipientCreateView(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = "core/recipients/create.html"
    success_url = reverse_lazy("core:recipient_create")


# model Mailing views
class MailingsView(ListView):
    model = Mailing
    template_name = "core/mailings/list.html"
    context_object_name = "mailings"


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "core/mailings/create.html"
    success_url = reverse_lazy("core:mailing_create")


# model Messages views
class MessagesView(ListView):
    model = Message
    template_name = "core/messages/list.html"
    context_object_name = "messages"
