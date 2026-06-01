from django import forms

from core.models import MailingRecipient


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['full_name', 'email', 'comment']