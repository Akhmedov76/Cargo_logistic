from django.contrib import admin
from api.services.models import ServicesModel


@admin.register(ServicesModel)
class ServicesModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions', 'is_active')
    search_fields = ('name', 'descriptions')
    ordering = ('name',)
