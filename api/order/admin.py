from django.contrib import admin
from api.order.models import DeliveryRequest, DeliveryForDrivers

admin.site.register(DeliveryRequest)
admin.site.register(DeliveryForDrivers)
