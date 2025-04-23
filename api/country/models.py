from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(_("Respublika nomi"), max_length=100)
    code = models.CharField(max_length=15, blank=True, )

    def __str__(self):
        return self.name


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(_("Viloyat nomi"), max_length=100)
    code = models.CharField(max_length=15, blank=True, )

    def __str__(self):
        return f"{self.name} ({self.country.name})"


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(_("Tuman nomi"), max_length=100)
    code = models.CharField(max_length=15, blank=True, )

    def __str__(self):
        return f"{self.name} ({self.region.name})"
