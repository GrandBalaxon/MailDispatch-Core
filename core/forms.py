from django import forms

from core.mixins import StyleFormMixin
from core.models import MailingRecipient, Mailing, Message


class MailingRecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['full_name', 'email', 'comment']


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'start_time', 'end_time', 'recipients']


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
