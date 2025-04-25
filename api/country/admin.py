from django.contrib import admin
from api.country.models import Region, District, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'country', 'lat', 'lon')
    search_fields = ('name', 'code')
    list_filter = ('country',)
    autocomplete_fields = ('country',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'code',)
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('region', 'name')
    autocomplete_fields = ('region',)
