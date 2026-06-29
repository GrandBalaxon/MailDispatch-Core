import ast

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    token = models.CharField(max_length=100, verbose_name="Токен верификации")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")

    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('manager', 'Менеджер')
    ]
    role = models.CharField(
        default='user',
        max_length=100,
        choices=ROLE_CHOICES,
        verbose_name="Роль"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
