from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.base.mixins import TimeModelMixin


class User(TimeModelMixin, AbstractUser):
    ROLE_CHOICES = (
        ('operator', 'Operator'),
        ('driver', 'Driver'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    company = models.CharField(_('Company name'), max_length=55, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
