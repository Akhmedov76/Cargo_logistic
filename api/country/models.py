from django.db import models
from django.utils.translation import gettext_lazy as _

from api.base import TimeModelMixin


class Country(models.Model):
    name = models.CharField(_("Respublika nomi"), max_length=100)
    code = models.CharField(max_length=15, blank=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Respublika")
        verbose_name_plural = _("Respublikalar")
        ordering = ('name',)


class Region(models.Model):
    name = models.CharField(_('Nomi'), max_length=255)
    code = models.CharField(max_length=50)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.country.name})"

    class Meta:
        verbose_name = _("Viloyat")
        verbose_name_plural = _("Viloyatlar")
        ordering = ('name',)


class District(TimeModelMixin):
    name = models.CharField(_('Nomi'), max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    coordinates = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=50)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Tuman")
        verbose_name_plural = _("Tumanlar")

    def __str__(self):
        return f"{self.name}/{self.region.name}/{self.region.country.name}"
