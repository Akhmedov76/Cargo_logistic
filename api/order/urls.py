from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.order.views import DeliveryOrderView, OrderCreateView

router = SimpleRouter()

router.register(r'order', DeliveryOrderView, basename='order')
router.register(r'create/delivery', OrderCreateView, basename='create')

urlpatterns = [
    path('', include(router.urls)),
]
