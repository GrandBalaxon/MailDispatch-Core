from django.db.models import Prefetch, Count, OuterRef, Subquery
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from core.forms import MailingRecipientForm
from core.models import Mailing, MailingRecipient


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


class MailingRecipientsView(ListView):
    model = MailingRecipient
    template_name = "core/mailing_recipients.html"
    context_object_name = "recipients"


class RecipientCreateView(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = "core/recipient_create.html"
    success_url = reverse_lazy("core:mailing_recipients")
