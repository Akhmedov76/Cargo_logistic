from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.order.models import AddCargo, DeliveryForDrivers
from api.order.serializers import OrderCargoSerializer, OrderCarrierSerializer


class CargoRequestView(ModelViewSet):
    queryset = AddCargo.objects.all()
    serializer_class = OrderCargoSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(query_serializer=None)
    @action(detail=False, methods=['get'], url_path='get-cargo-owner')
    def get_order(self, request):
        if request.user.is_staff:
            order = AddCargo.objects.all()
        else:
            order = AddCargo.objects.filter(contact=request.user)
        serializer = OrderCargoSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=OrderCargoSerializer)
    @action(detail=False, methods=['post'], url_path='create-cargo-owner')
    def create_order(self, request):
        serializer = OrderCargoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role=request.user)
            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=OrderCargoSerializer)
    @action(detail=False, methods=['put'], url_path='update-cargo-owner')
    def update_order(self, request):
        try:
            if request.user.is_staff:
                order = AddCargo.objects.get(id=request.data.get('id'))
            else:
                order = AddCargo.objects.get(id=request.data.get('id'), contact=request.user)
        except AddCargo.DoesNotExist:
            return Response({"error": "Cargo not found or access denied"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderCargoSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryOrderView(ModelViewSet):
    queryset = DeliveryForDrivers.objects.all()
    serializer_class = OrderCarrierSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(query_serializer=OrderCarrierSerializer)
    @action(detail=False, methods=['get'], url_path='get-driver-order')
    def get_order(self, request):
        order = DeliveryForDrivers.objects.filter(role=request.user.role)
        serializer = OrderCarrierSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(query_serializer=OrderCarrierSerializer)
    @action(detail=False, methods=['post'], url_path='create-driver-order')
    def create_order(self, request):
        serializer = OrderCarrierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
