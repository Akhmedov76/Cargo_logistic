from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.base.paginator import CustomPagination
from api.order.models import AddCargo, DeliveryForDrivers
from api.order.serializers import OrderCargoSerializer, OrderCarrierSerializer


class CargoRequestView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    queryset = AddCargo.objects.all()
    serializer_class = OrderCargoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(query_serializer=None)
    @action(detail=False, methods=['get'], url_path='get-cargo-owner')
    def get_cargo_list(self, request, *args, **kwargs):
        serialzer = OrderCargoSerializer(self.queryset, many=True)
        serialzer.is_valid()


    @swagger_auto_schema(request_body=OrderCargoSerializer)
    @action(detail=False, methods=['post'], url_path='create-cargo-owner')
    def create_order(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contact=request.user)
            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryOrderView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    queryset = DeliveryForDrivers.objects.all()
    serializer_class = OrderCarrierSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(query_serializer=None)
    @action(detail=False, methods=['get'], url_path='get-driver-order')
    def get_order(self, request):
        if request.user.is_staff:
            order = DeliveryForDrivers.objects.all()
        else:
            order = DeliveryForDrivers.objects.filter(contact=request.user)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(order, request)
        serializer = self.get_serializer(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=OrderCarrierSerializer)
    @action(detail=False, methods=['post'], url_path='create-driver-order')
    def create_order(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contact=request.user)
            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
