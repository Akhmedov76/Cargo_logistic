from django.contrib import admin
from api.order.models import AddCargo, DeliveryForDrivers


@admin.register(AddCargo)
class DeliveryRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cargo', 'volume', 'when', 'loading', 'unloading', 'services','contact', 'GPS_monitoring',
        'bid_currency', 'bid_price', 'price_in_UZS', 'created_at', 'updated_at')
    list_filter = ('contact', 'when', 'loading', 'unloading', 'bid_currency')
    search_fields = ('loading__name', 'unloading__name',  'contact__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DeliveryForDrivers)
class DeliveryForDriversAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'contact', 'loading', 'vehicle', 'body_volume', 'where', 'where_to', 'company', 'created_at', 'updated_at')
    list_filter = ('contact', 'company', 'loading', 'vehicle', 'where', 'where_to')
    search_fields = ('contact__email', 'vehicle', 'company', 'where__name', 'where_to__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
