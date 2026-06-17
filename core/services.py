from django.conf import settings
from django.core.mail import send_mail
from .models import Mailing, MailingAttempt


def run_mailing(mailing: Mailing) -> None:
    """Запускает ручную рассылку."""
    if mailing.status != "launched":
        raise ValueError(f"Ручная рассылка доступна лишь для рассылок со статусом 'запущена'.")

    recipients = mailing.recipients.all()
    email_list = [recipient.email for recipient in recipients]

    try:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email_list,
            fail_silently=False,
        )
        MailingAttempt.objects.create(
            mailing=mailing,
            status='successful',
            server_response='OK'
        )

    except Exception as e:
        MailingAttempt.objects.create(
            mailing=mailing,
            status='not successful',
            server_response=str(e)
        )
