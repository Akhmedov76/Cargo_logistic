from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.order.views import CargoRequestView, DeliveryOrderView

router = SimpleRouter()

router.register(r'cargos', CargoRequestView, basename='delivery')
router.register(r'driver', DeliveryOrderView, basename='driver')

urlpatterns = [
    path('', include(router.urls)),
]
