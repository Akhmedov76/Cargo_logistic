from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.base.paginator import CustomPagination
from api.order.models import AddCargo, DeliveryForDrivers
from api.order.serializers import OrderCargoSerializer, OrderCarrierSerializer, LocationInputSerializer
from api.order.services import match_where_to_driver, match_where_to_cargo, get_locations_cargo, get_locations_driver


class CargoRequestView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    queryset = AddCargo.objects.all()
    serializer_class = OrderCargoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(query_serializer=OrderCargoSerializer)
    @action(detail=False, methods=['GET'], url_path='get-cargo')
    def get_cargo_list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = AddCargo.objects.all()
        else:
            queryset = AddCargo.objects.filter(contact=request.user)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=OrderCargoSerializer)
    @action(detail=False, methods=['POST'], url_path='create-cargo')
    def create_cargo(self, request):
        serializer = OrderCargoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        cargo = AddCargo.objects.create(**validated_data, contact=request.user)
        response_serializer = OrderCargoSerializer(cargo)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=LocationInputSerializer)
    @action(detail=False, methods=['POST'], url_path='search-matched-drivers')
    def get_where_where_to(self, request):
        serializer = LocationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        loading_location = validated_data.get('loading_location')
        unloading_location = validated_data.get('unloading_location')
        volume = validated_data.get('volume')
        if volume in ["", None]:
            volume = None

        cargo_queryset = AddCargo.objects.filter(
            loading__name=loading_location,
            unloading__name=unloading_location
        )

        if volume is not None:
            cargo_queryset = cargo_queryset.filter(volume__gte=volume)

        cargo = cargo_queryset.first()

        if not cargo:
            return Response({"message": "No matching cargo found."}, status=status.HTTP_404_NOT_FOUND)

        matched_where_where_to = match_where_to_driver(cargo)

        datas = [
            {
                'driver_id': driver.id,
                'contact': driver.contact.full_name() if driver.contact else None,
                'phone_number': driver.contact.phone_number if driver.contact else None,
                'where': driver.where.name if driver.where else None,
                'where_to': driver.where_to.name if driver.where_to else None,
                'car_model': driver.car_model if driver.car_model else None,
                'distance_km': driver.distance_km if driver.distance_km else None,
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

    @swagger_auto_schema(request_body=LocationInputSerializer)
    @action(detail=False, methods=['POST'], url_path='search-cargo-by-locations')
    def get_cargo_by_where_where_to(self, request):
        serializer = LocationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        loading_location = validated_data.get('loading_location')
        unloading_location = validated_data.get('unloading_location')
        volume = validated_data.get('volume')
        if volume in ["", None]:
            volume = None

        cargo_queryset = AddCargo.objects.filter(
            loading__name=loading_location,
            unloading__name=unloading_location
        )
        if volume is not None:
            cargo_queryset = cargo_queryset.filter(volume__gte=volume)

        cargo = cargo_queryset.first()

        get_cargo = get_locations_cargo(cargo)

        datas = [
            {
                'cargo_id': cargo.id,
                'contact': cargo.contact.full_name() if cargo.contact else None,
                'phone_number': cargo.contact.phone_number if cargo.contact else None,
                'loading': cargo.loading.name if cargo.loading else None,
                'unloading': cargo.unloading.name if cargo.unloading else None,
                'caro_type': cargo.cargo_type.name if cargo.cargo_type else None,
                'services': cargo.services.name if cargo.services else None,
                'GPS_monitoring': cargo.GPS_monitoring if cargo.GPS_monitoring else None,
                'distance_km': cargo.distance_km if cargo.distance_km else None,
                'bid_currency': cargo.bid_currency if cargo.bid_currency else None,
                'bid_price': cargo.bid_price if cargo.bid_price else None,
                'price_in_UZS': cargo.price_in_UZS if cargo.price_in_UZS else None,
                'weight': cargo.weight if cargo.weight else None,
                'volume': cargo.volume if cargo.volume else None,
                'length': cargo.length if cargo.length else None,
                'width': cargo.width if cargo.width else None,
                'height': cargo.height if cargo.height else None,

            } for cargo in get_cargo
        ]

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

    @swagger_auto_schema(request_body=LocationInputSerializer)
    @action(detail=False, methods=['post'], url_path='search-matched-cargo')
    def get_where_where_to(self, request):
        serializer = LocationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        where = validated_data.get('loading_location')
        where_to = validated_data.get('unloading_location')
        volume = validated_data.get('volume')

        if volume in ["", None]:
            volume = None

        driver_queryset = DeliveryForDrivers.objects.filter(
            where__name=where,
            where_to__name=where_to
        )
        if volume is not None:
            driver_queryset = driver_queryset.filter(volume__gte=volume)

        driver = driver_queryset.first()
        print(driver)
        if not driver:
            return Response({"message": "No matching driver found."}, status=status.HTTP_404_NOT_FOUND)

        matched_where_where_to = match_where_to_cargo(driver)
        datas = [
            {
                'cargo_id': cargo.id,
                'contact': cargo.contact.full_name() if cargo.contact else None,
                'phone_number': cargo.contact.phone_number if cargo.contact else None,
                'car_type': cargo.cargo_type.name,
                'services': cargo.services.name if cargo.services else None,
                'where': cargo.loading.name if cargo.loading else None,
                'where_to': cargo.unloading.name if cargo.unloading else None,
                'when': cargo.when if cargo.when else None,
                'GPS_monitoring': cargo.GPS_monitoring if cargo.GPS_monitoring else None,
                'bid_price': cargo.bid_price if cargo.bid_price else None,
                'price_in_UZS': cargo.price_in_UZS if cargo.price_in_UZS else None,
                'volume m3': cargo.volume if cargo.volume else None,
                'weight kg': cargo.weight if cargo.weight else None,
                'length': cargo.length,
                'width': cargo.width,
                'height': cargo.height,

            }
            for cargo in matched_where_where_to
        ]

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(datas, request)
        return paginator.get_paginated_response(result_page)

    @swagger_auto_schema(request_body=LocationInputSerializer)
    @action(detail=False, methods=['post'], url_path='search-driver-by-locations')
    def get_cargo_by_where_where_to(self, request):
        serializer = LocationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        where = validated_data.get('loading_location')
        where_to = validated_data.get('unloading_location')
        volume = validated_data.get('volume')

        if volume in ["", None]:
            volume = None

        driver_queryset = DeliveryForDrivers.objects.filter(
            where__name=where,
            where_to__name=where_to
        )
        if volume is not None:
            driver_queryset = driver_queryset.filter(volume__gte=volume)

        driver = driver_queryset.first()

        get_cargo = get_locations_driver(driver)

        if not get_cargo:
            return Response({"message": "No matching cargo found."}, status=status.HTTP_404_NOT_FOUND)

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
            for driver in get_cargo
        ]
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(datas, request)
        return paginator.get_paginated_response(result_page)
