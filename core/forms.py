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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['recipients'].queryset = MailingRecipient.objects.filter(added_by=self.user)
            self.fields['message'].queryset = Message.objects.filter(author=self.user)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
