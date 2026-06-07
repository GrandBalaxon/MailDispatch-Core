import datetime

from django.db import models
from django.utils.timezone import now


class MailingRecipient(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О.")
    email = models.EmailField(unique=True)
    comment = models.TextField(max_length=500, null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "получатель рассылки"
        verbose_name_plural = "получатели рассылки"


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("launched", "Запущена"),
        ("finished", "Завершена")
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(default=STATUS_CHOICES[0], choices=STATUS_CHOICES, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING)
    recipients = models.ManyToManyField(MailingRecipient, related_name="mailings")

    def __str__(self):
        return f"{self.message} - {self.status} - Получателей: {len(self.recipients.all())}"

    def update_status(self) -> None:
        """
        Метод проверки текущего времени, сравнения его с временем начала и окончания рассылки и обновления статуса рассылки.
        """
        current_time = now()
        if self.start_time < current_time < self.end_time:
            self.status = "launched"
        elif self.end_time <= current_time:
            self.status = "finished"
        self.save()

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"


class MailingAttempt(models.Model):
    attempt_time = models.DateTimeField(auto_now=True, verbose_name="Дата и время попытки")
    status = models.CharField(
        null=False,
        blank=False,
        choices=[
            ("successful", "Успешно"),
            ("not successful", "Не успешно"),
        ],
        verbose_name="Статус"
    )
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="attempts")

    def __str__(self):
        return f"{self.attempt_time} - {self.status}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
