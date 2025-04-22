from django.db import models

from api.base.mixins import TimeModelMixin


class CargoElements(TimeModelMixin, models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    descriptions = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.descriptions})"

    class Meta:
        verbose_name = 'Element'
        verbose_name_plural = 'Elements'
