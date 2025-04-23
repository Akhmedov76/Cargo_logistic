from django.db import models
from django.utils.translation import gettext_lazy as _

from api.base.currency_service import get_currency_rate
from api.base.mixins import TimeModelMixin
from api.cargo_base.models import CargoType
from api.country.models import District
from api.services.models import ServicesModel
from api.users.models import User


class AddCargo(TimeModelMixin, models.Model):
    when_loading = [
        ('ready_to_download', 'Ready to download'),
        ('permanent', 'Permanent'),
        ('no_load', 'No load')
    ]
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RUB', 'RUB'),
        ('GBP', 'GBP'),
        ('CNY', 'CNY'),
        ('KZT', 'KZT'),
        ('SUM', 'UZS')
    ]
    cargo = models.ForeignKey(CargoType, on_delete=models.CASCADE, blank=True, null=True)
    weight = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    volume = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='m3')

    when = models.CharField(max_length=30, blank=True, choices=when_loading)
    loading = models.ForeignKey(District, on_delete=models.CASCADE, null=True,
                                related_name='loading')
    unloading = models.ForeignKey(District, on_delete=models.CASCADE, null=True,
                                  related_name='unloading')
    services = models.ForeignKey(ServicesModel, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='role')
    GPS_monitoring = models.BooleanField(default=False)
    contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='contact')

    bid_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='SUM')
    bid_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'

    def bid_in_uzs(self):
        if self.bid_currency == 'SUM':
            return self.bid_price
        rate = get_currency_rate(self.bid_currency)
        print(rate)
        if rate:
            return self.bid_price * rate
        return 0


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
