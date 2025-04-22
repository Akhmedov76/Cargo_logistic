from django.db import models
from django.utils.translation import gettext_lazy as _

from api.base.mixins import TimeModelMixin
from api.cargo_base.models import CargoElements
from api.country.models import District
from api.services.models import ServicesModel
from api.users.models import User


class DeliveryRequest(TimeModelMixin, models.Model):
    when_loading = [
        ('ready to load', 'Ready to load'),
        ('permanent', 'Permanent'),
        ('no load', 'No load')
    ]
    cargo = models.ForeignKey(CargoElements, on_delete=models.CASCADE, blank=True, null=True)
    weight = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    capacity = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    when = models.CharField(max_length=255, blank=True, choices=when_loading)
    loading = models.ForeignKey(District, on_delete=models.CASCADE, null=True,
                                related_name='deliveryrequest_loading')
    download = models.ForeignKey(District, on_delete=models.CASCADE, null=True,
                                 related_name='deliveryrequest_download')
    services = models.ForeignKey(ServicesModel, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'


class DeliveryForDrivers(TimeModelMixin, models.Model):
    Loading_choice = [
        ('from above', 'From above'),
        ('from the side', 'From the side'),
        ('from behind', 'From behind'),
        ('with full awning', 'With full awning'),
        ('with the removal of crossbars', 'With the removal of crossbars'),
        ('electricity', 'electricity')
    ]
    role = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    loading = models.CharField(choices=Loading_choice, max_length=255, blank=True, null=True)
    vehicle = models.CharField(_('Vehicle'), max_length=55, blank=True, null=True)
    body_volume = models.DecimalField(_('Volume'), max_digits=12, decimal_places=2, null=True, blank=True)
    where = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    where_to = models.ForeignKey(District, on_delete=models.CASCADE, null=True,
                                 related_name='delivery_where_to')
    company = models.CharField(_('company'), max_length=55, blank=True, null=True)

    def __str__(self):
        return self.loading if self.loading else "No loading choice"

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
