from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager
from django.core.validators import MaxLengthValidator, MinLengthValidator


class CustomUser(AbstractUser):
    """Модель для пользователей"""

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    phone_number = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(7)],
        unique=True)

    birth_day = models.DateField(
        null=True,
        blank=True)

    balance = models.PositiveIntegerField(default=0)

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
