from django import forms

from core.models import MailingRecipient, Mailing


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['full_name', 'email', 'comment']


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'start_time', 'end_time', 'recipients']
