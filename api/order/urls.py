from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.order.views import DeliveryOrderView

router = SimpleRouter()

router.register(r'order', DeliveryOrderView, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]
