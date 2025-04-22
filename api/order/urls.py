from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.order.views import DeliveryRequestView, DeliveryOrderView

router = SimpleRouter()

router.register(r'order_delivery', DeliveryRequestView, basename='delivery')
router.register(r'driver', DeliveryOrderView, basename='driver')

urlpatterns = [
    path('', include(router.urls)),
]
