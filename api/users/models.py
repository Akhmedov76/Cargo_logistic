from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.base.mixins import TimeModelMixin


class User(TimeModelMixin, AbstractUser):
    ROLE_CHOICES = (
        ('dispatcher', 'Dispatcher'),
        ('carrier', 'Carrier'),
        ('cargo owner', 'Cargo owner'),
        ('forwarder', 'Forwarder'),
    )
    role = models.CharField(choices=ROLE_CHOICES, blank=True, null=True, default='carrier')
    middle_name = models.CharField(max_length=55, blank=True, null=True)
    phone_number = models.CharField(help_text='+998 1234567', max_length=20, unique=True, null=True)
    passport_serial = models.CharField(max_length=10, blank=True, null=True, help_text="AB")
    passport_number = models.CharField(max_length=10, blank=True, null=True, help_text="1234567890")
    date_given = models.DateField(blank=True, null=True)
    given_by_whom = models.CharField(max_length=55, blank=True, null=True)
    passport_file = models.FileField(upload_to='users/passport/', blank=True, null=True)
    drivers_license_serial_number = models.CharField(max_length=25, blank=True, null=True)
    date_of_issue_license = models.DateField(blank=True, null=True)
    drivers_license_file = models.FileField(upload_to='users/drivers_license/', blank=True, null=True)
    is_agree = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
