from django.contrib import admin

from core.models import MailingRecipient, Message, Mailing


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body')
    search_fields = ('id', 'subject')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'message', 'start_time', 'end_time', 'recipients_count')
    list_filter = ("status",)

    def recipients_count(self, obj):
        return obj.recipients.count()

    recipients_count.short_description = 'Количество получателей'
