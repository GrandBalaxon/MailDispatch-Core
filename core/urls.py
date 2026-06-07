from django.urls import path
from .views import *
from .apps import CoreConfig

app_name = CoreConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),

    path('mailing/list/', MailingsView.as_view(), name="mailing_list"),
    path('mailing/add/', MailingCreateView.as_view(), name="mailing_create"),

    path('mailing/recipients/', MailingRecipientsView.as_view(), name="recipient_list"),
    path('mailing/recipients/add/', RecipientCreateView.as_view(), name="recipient_create"),

    path('mailing/messages/', MessagesView.as_view(), name="message_list"),
    path('mailing/messages/add/', MessageCreateView.as_view(), name="message_create"),
]
