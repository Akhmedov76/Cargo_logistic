from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.order.views import CargoRequestView, DeliveryOrderView

router = SimpleRouter()

router.register(r'cargo', CargoRequestView, basename='delivery')
router.register(r'driver', DeliveryOrderView, basename='driver')

urlpatterns = [
    path('', include(router.urls)),
]
