from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.order.models import DeliveryRequest, DeliveryForDrivers
from api.order.serializers import OrderSerializer, OrderCreateSerializer


class DeliveryRequestView(ModelViewSet):
    queryset = DeliveryRequest.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(query_serializer=OrderSerializer)
    @action(detail=False, methods=['get'], url_path='get-order')
    def get_order(self, request):
        order = DeliveryRequest.objects.filter(role=request.user.role)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryOrderView(ModelViewSet):
    queryset = DeliveryForDrivers.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(query_serializer=OrderCreateSerializer)
    @action(detail=False, methods=['get'], url_path='get-driver-order')
    def get_order(self, request):
        order = DeliveryForDrivers.objects.filter(role=request.user.role)
        serializer = OrderCreateSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(query_serializer=OrderCreateSerializer)
    @action(detail=False, methods=['post'], url_path='create-driver-order')
    def create_order(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
