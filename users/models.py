from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    token = models.CharField(max_length=100, verbose_name="Токен верификации")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
