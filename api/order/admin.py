from django.contrib import admin
from api.order.models import AddCargo, DeliveryForDrivers


@admin.register(AddCargo)
class CargoRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cargo_type', 'when', 'loading', 'unloading', 'services', 'contact', 'GPS_monitoring',
        'bid_currency', 'bid_price', 'price_in_UZS', 'volume', 'width', 'length', 'height', 'created_at', 'updated_at')
    list_filter = ('contact', 'when', 'loading', 'unloading', 'bid_currency')
    search_fields = ('loading__name', 'unloading__name', 'contact__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DeliveryForDrivers)
class DeliveryForDriversAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'loading', 'contact', 'weight', 'length', 'width', 'height', 'volume',
        'where', 'where_to', 'GPS_monitoring', 'bid_currency', 'bid_price', 'price_in_UZS',
        'created_at', 'updated_at')
    list_filter = (
        'contact', 'loading', 'where', 'where_to', 'GPS_monitoring', 'bid_currency')
    search_fields = (
        'contact__email', 'contact__username',
        'where__name', 'where_to__name', 'loading', 'bid_currency'
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
