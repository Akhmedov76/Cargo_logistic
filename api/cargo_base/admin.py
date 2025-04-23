from django.contrib import admin
from api.cargo_base.models import CargoType


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions',)
    search_fields = ('name', 'code')
    ordering = ('name',)
