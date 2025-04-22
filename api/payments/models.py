from django.db import models
from django.utils.translation import gettext_lazy as _

from api.base.mixins import TimeModelMixin


class PaymentsModel(TimeModelMixin, models.Model):
    amount = models.DecimalField(_('Service price'), max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    paid_at_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}"

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
