from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from api.order.views import CargoRequestView, DeliveryOrderView

router = DefaultRouter()

router.register(r'cargo', CargoRequestView, basename='delivery')
router.register(r'driver', DeliveryOrderView, basename='driver')

urlpatterns = [
    path('stations/', include(router.urls)),
]
