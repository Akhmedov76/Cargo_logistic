from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.order.views import CargoRequestView, DeliveryOrderView

router = DefaultRouter()

router.register(r'cargo', CargoRequestView, basename='cargo')
router.register(r'driver', DeliveryOrderView, basename='driver')

urlpatterns = [
    path('', include(router.urls)),
]
