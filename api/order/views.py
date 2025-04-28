from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.base.paginator import CustomPagination
from api.order.models import AddCargo, DeliveryForDrivers
from api.order.serializers import OrderCargoSerializer, OrderCarrierSerializer, LocationInputSerializer
from api.order.services import match_where_where_to_driver


# def your_view(request):
#     from django.conf import settings
#     return render(request, '', {
#         'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
#     })


class CargoRequestView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    queryset = AddCargo.objects.all()
    serializer_class = OrderCargoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'], url_path='get-cargo-owner')
    def get_cargo_list(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # @action(detail=False, methods=['get'], url_path='cargo/get-drivers')
    # def get_matched_drivers(self, request):
    #     serializer = OrderCargoSerializer(data=request.query_params)
    #     serializer.is_valid(raise_exception=True)
    #     validated_data = serializer.validated_data
    #
    #     cargo = AddCargo(**validated_data)
    #
    #     matched_drivers = match_cargo_to_driver(cargo)
    #
    #     data = [
    #         {
    #             'driver_id': driver.id,
    #             'contact': driver.contact.full_name() if driver.contact else None,
    #             'phone_number': driver.contact.phone_number if driver.contact else None,
    #             'where': driver.where.name if driver.where else None,
    #             'where_to': driver.where_to.name if driver.where_to else None,
    #             'car_model': driver.car_model if driver.car_model else None,
    #             'weight_kg': driver.weight if driver.weight else None,
    #             'volume_m3': driver.volume if driver.volume else None,
    #             'width': driver.width if driver.width else None,
    #             'length': driver.length if driver.length else None,
    #             'height': driver.height if driver.height else None,
    #             'bid_price': driver.bid_price if driver.bid_price else None,
    #             'price_in_UZS': driver.price_in_UZS if driver.price_in_UZS else None,
    #         }
    #         for driver in matched_drivers
    #     ]
    #     paginator = self.pagination_class()
    #     result_page = paginator.paginate_queryset(data, request)
    #
    #     return paginator.get_paginated_response(result_page)

    @swagger_auto_schema(request_body=LocationInputSerializer)
    @action(detail=False, methods=['POST'], url_path='cargo/get-matched-drivers')
    def get_where_where_to(self, request):
        serializer = LocationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        loading_location = validated_data['loading_location']
        unloading_location = validated_data['unloading_location']
        volume = validated_data['volume']

        cargo = AddCargo.objects.filter(volume, loading__name=loading_location,
                                        unloading__name=unloading_location).first()
        if not cargo:
            return Response({"message": "No matching cargo found."}, status=status.HTTP_404_NOT_FOUND)

        matched_where_where_to = match_where_where_to_driver(cargo)

        datas = [
            {
                'driver_id': driver.id,
                'contact': driver.contact.full_name() if driver.contact else None,
                'phone_number': driver.contact.phone_number if driver.contact else None,
                'where': driver.where.name if driver.where else None,
                'where_to': driver.where_to.name if driver.where_to else None,
                'car_model': driver.car_model if driver.car_model else None,
                'weight_kg': driver.weight if driver.weight else None,
                'volume_m3': driver.volume if driver.volume else None,
                'width': driver.width if driver.width else None,
                'length': driver.length if driver.length else None,
                'height': driver.height if driver.height else None,
                'bid_price': driver.bid_price if driver.bid_price else None,
                'price_in_UZS': driver.price_in_UZS if driver.price_in_UZS else None,
            }
            for driver in matched_where_where_to
        ]
        if not datas:
            return Response({"message": "No matched drivers found."}, status=status.HTTP_404_NOT_FOUND)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(datas, request)
        return paginator.get_paginated_response(result_page)


class DeliveryOrderView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    queryset = DeliveryForDrivers.objects.all()
    serializer_class = OrderCarrierSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

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
