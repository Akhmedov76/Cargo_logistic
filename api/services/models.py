from django.db import models
from django.utils.translation import gettext_lazy as _

from api.base.mixins import TimeModelMixin


class ServicesModel(TimeModelMixin, models.Model):
    name = models.CharField(_('Service name'), max_length=55, blank=True, null=True)
    descriptions = models.TextField(_('Service descriptions'), blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}  ({self.descriptions})"

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
