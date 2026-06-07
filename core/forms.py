from django import forms

from core.models import MailingRecipient, Mailing, Message


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['full_name', 'email', 'comment']


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'start_time', 'end_time', 'recipients']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
