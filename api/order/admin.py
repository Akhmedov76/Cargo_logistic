from django.contrib import admin
from api.order.models import AddCargo, DeliveryForDrivers


@admin.register(AddCargo)
class DeliveryRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'cargo', 'weight', 'volume', 'when', 'loading', 'download', 'services', 'role')
    list_filter = ('role', 'cargo')


@admin.register(DeliveryForDrivers)
class DeliveryForDriversAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'loading', 'vehicle', 'body_volume', 'where', 'where_to', 'company')
    list_filter = ('role', 'company', 'loading', 'vehicle',)
