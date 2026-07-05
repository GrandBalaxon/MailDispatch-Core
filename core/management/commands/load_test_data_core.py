from django.core.management import BaseCommand, call_command

from core.models import MailingRecipient, Message, Mailing, MailingAttempt


class Command(BaseCommand):
    help = 'Загружает тестовые данные для приложения core.'

    def handle(self, *args, **kwargs):
        MailingRecipient.objects.all().delete()
        Message.objects.all().delete()
        Mailing.objects.all().delete()
        MailingAttempt.objects.all().delete()

        call_command('loaddata', 'core/fixtures/initial_core_data.json')

        self.stdout.write(self.style.SUCCESS('Test data for CORE app loaded successfully.'))
