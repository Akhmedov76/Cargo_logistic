from django.contrib import admin

from api.order.models import AddCargo, DeliveryForDrivers


@admin.register(AddCargo)
class CargoRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cargo_type_name', 'when', 'loading', 'unloading', 'services_name', 'contact', 'GPS_monitoring',
        'bid_currency', 'bid_price', 'price_in_UZS', 'weight', 'volume', 'width', 'length', 'height', 'created_at',
        'updated_at')
    list_filter = ('contact', 'when', 'loading', 'unloading', 'bid_currency')
    search_fields = ('loading__name', 'unloading__name', 'contact__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def cargo_type_name(self, obj):
        return obj.cargo_type.name

    cargo_type_name.short_description = "Cargo Type"

    def services_name(self, obj):
        return obj.services.name

    services_name.short_description = "Services"


@admin.register(DeliveryForDrivers)
class DeliveryForDriversAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'loading', 'contact', 'where', 'where_to', 'GPS_monitoring', 'bid_currency', 'bid_price', 'price_in_UZS',
        'weight', 'length', 'width', 'height', 'volume',
        'created_at', 'updated_at')
    list_filter = (
        'contact', 'loading', 'where', 'where_to', 'GPS_monitoring', 'bid_currency')
    search_fields = (
        'contact__email', 'contact__username',
        'where__name', 'where_to__name', 'loading', 'bid_currency'
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
