from django.contrib import admin
from api.order.models import AddCargo, DeliveryForDrivers


@admin.register(AddCargo)
class DeliveryRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cargo', 'weight', 'volume', 'when', 'loading', 'unloading', 'services', 'role', 'GPS_monitoring',
        'contact', 'bid_currency', 'bid_price', 'price_in_UZS', 'created_at', 'updated_at')
    list_filter = ('role', 'when', 'loading', 'unloading', 'bid_currency')
    search_fields = ('loading__name', 'unloading__name', 'role__username', 'contact__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DeliveryForDrivers)
class DeliveryForDriversAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'role', 'loading', 'vehicle', 'body_volume', 'where', 'where_to', 'company', 'created_at', 'updated_at')
    list_filter = ('role', 'company', 'loading', 'vehicle', 'where', 'where_to')
    search_fields = ('role__username', 'vehicle', 'company', 'where__name', 'where_to__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
