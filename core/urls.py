from django.urls import path
from .views import *
from .apps import CoreConfig

app_name = CoreConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),

    path('mailing/list/', MailingsView.as_view(), name="mailing_list"),
    path('mailing/add/', MailingCreateView.as_view(), name="mailing_create"),
    path('mailing/<int:pk>/', MailingDetailsView.as_view(), name="mailing_details"),
    path('mailing/<int:pk>/edit/', MailingUpdateView.as_view(), name="mailing_edit"),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name="mailing_delete"),

    path('mailing/recipients/', MailingRecipientsView.as_view(), name="recipient_list"),
    path('mailing/recipients/add/', RecipientCreateView.as_view(), name="recipient_create"),
    path('mailing/recipients/<int:pk>/', RecipientDetailsView.as_view(), name="recipient_details"),
    path('mailing/recipients/<int:pk>/edit/', RecipientUpdateView.as_view(), name="recipient_edit"),
    path('mailing/recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name="recipient_delete"),

    path('mailing/messages/', MessagesView.as_view(), name="message_list"),
    path('mailing/messages/add/', MessageCreateView.as_view(), name="message_create"),
    path('mailing/messages/<int:pk>/', MessageDetailsView.as_view(), name="message_details"),
    path('mailing/messages/<int:pk>/edit/', MessageUpdateView.as_view(), name="message_edit"),
    path('mailing/messages/<int:pk>/delete/', MessageDeleteView.as_view(), name="message_delete"),
]
