from django.contrib import admin
from api.country.models import Region, District, Country

admin.site.register(Region)
admin.site.register(District)
admin.site.register(Country)
