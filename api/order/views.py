from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.order.models import DeliveryRequest, DeliveryForDrivers
from api.order.serializers import OrderSerializer, OrderCreateSerializer


class DeliveryOrderView(ModelViewSet):
    queryset = DeliveryRequest.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(role=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return self.queryset.filter(role=user)
        return self.queryset


class OrderCreateView(ModelViewSet):
    queryset = DeliveryForDrivers.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(role=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return self.queryset.filter(role=user)
        return self.queryset
