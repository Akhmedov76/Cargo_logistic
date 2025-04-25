from django.db import models
from django.utils.translation import gettext_lazy as _

from api.base.currency_service import get_currency_rate
from api.base.mixins import TimeModelMixin
from api.cargo_base.models import CargoType
from api.country.models import District, Country, Region
from api.services.models import ServicesModel
from api.users.models import User

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


class AddCargo(TimeModelMixin, models.Model):
    cargo_type = models.ForeignKey(CargoType, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.DecimalField(max_digits=12, decimal_places=2, help_text='kg')
    length = models.DecimalField(max_digits=12, decimal_places=2, help_text='m')
    width = models.DecimalField(max_digits=12, decimal_places=2, help_text='m')
    height = models.DecimalField(max_digits=12, decimal_places=2, help_text='m')
    volume = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='m3')
    when = models.CharField(max_length=30, blank=True, choices=when_loading)
    loading = models.ForeignKey(District, on_delete=models.CASCADE, null=True,
                                related_name='loading')
    unloading = models.ForeignKey(District, on_delete=models.CASCADE, null=True,
                                  related_name='unloading')
    services = models.ForeignKey(ServicesModel, on_delete=models.CASCADE, )
    contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='cargo_roles')
    GPS_monitoring = models.BooleanField(default=False)

    bid_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='SUM')
    bid_price = models.DecimalField(max_digits=12, decimal_places=2)
    price_in_UZS = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.contact} - {self.loading} to {self.unloading}"

    class Meta:
        verbose_name = _('Cargo')
        verbose_name_plural = _('Cargo')

    def save(self, *args, **kwargs):
        if self.width and self.length and self.height:
            self.volume = self.width * self.length * self.height
        else:
            self.volume = None

        if self.bid_currency == 'SUM':
            self.price_in_UZS = self.bid_price
        else:
            rate = get_currency_rate(self.bid_currency)
            if rate and self.bid_price:
                self.price_in_UZS = float(self.bid_price) * rate
        super().save(*args, **kwargs)


class DeliveryForDrivers(TimeModelMixin, models.Model):
    CAR_TYPE = [
        ('truck', 'Truck'),
        ('semitrailer', 'Semitrailer'),
    ]
    CAR_BODY_TYPE = [
        ('hatchback', 'Hatchback'),
        ('sedan', 'Sedan'),
        ('van', 'Van'),
        ('minivan', 'Minivan'),
        ('pickup', 'Pickup'),
        ('trailer', 'Trailer'),
        ('flatbed', 'Flatbed'),
        ('wagon', 'Wagon'),
        ('bus', 'Bus'),
        ('container', 'Container'),
        ('auto transporter', 'Auto transporter'),
        ('gas carrier', 'Gas carrier'),
    ]
    Loading_choice = [
        ('top', 'Top'),
        ('lateral', 'Lateral'),
        ('back', 'Back'),
        ('with full awning', 'With full awning'),
        ('with the removal of crossbars', 'With the removal of crossbars'),
    ]
    car_model = models.CharField(choices=CAR_TYPE, max_length=255, blank=True, null=True)
    if car_model == 'truck':
        car_body_type = models.CharField(choices=CAR_BODY_TYPE, max_length=255, )

    loading = models.CharField(choices=Loading_choice, max_length=255, blank=True, null=True)
    weight = models.DecimalField(max_digits=12, decimal_places=2, help_text='kg')
    length = models.DecimalField(max_digits=12, decimal_places=2, help_text='m')
    width = models.DecimalField(max_digits=12, decimal_places=2, help_text='m')
    height = models.DecimalField(max_digits=12, decimal_places=2, help_text='m')
    volume = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='m3')
    GPS_monitoring = models.BooleanField(default=False)
    when = models.CharField(max_length=30, blank=True, choices=when_loading)
    where = models.ForeignKey(District, on_delete=models.CASCADE, )
    where_to = models.ForeignKey(District, on_delete=models.CASCADE, related_name='delivery_where_to')

    bid_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='SUM')
    bid_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_in_UZS = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.contact} - {self.where} to {self.where_to}"

    class Meta:
        verbose_name = _('Driver')
        verbose_name_plural = _('Drivers')
