from decimal import InvalidOperation, Decimal

from rest_framework import serializers

from api.base.base import Loading_choice
from api.country.models import District
from api.order.models import AddCargo, DeliveryForDrivers
from api.users.models import User


class OrderCargoSerializer(serializers.ModelSerializer):
    cargo_type = serializers.SlugRelatedField(read_only=True, slug_field='name')
    services = serializers.SlugRelatedField(read_only=True, slug_field='name')
    loading_body = serializers.ChoiceField(choices=Loading_choice, required=False)
    loading = serializers.SlugRelatedField(read_only=True, slug_field='name')
    unloading = serializers.SlugRelatedField(read_only=True, slug_field='name')
    contact = serializers.SlugRelatedField(read_only=True, slug_field='email')
    weight = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    length = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    width = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    height = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    volume = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)

    bid_currency = serializers.CharField(required=False, max_length=10)
    bid_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    price_in_UZS = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    GPS_monitoring = serializers.BooleanField(required=False)
    distance_km = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    class Meta:
        model = AddCargo
        fields = [
            'id',
            'cargo_type',
            'loading',
            'unloading',
            'services',
            'loading_body',
            'contact',
            'when',
            'when_to',
            'GPS_monitoring',
            'bid_currency',
            'bid_price',
            'price_in_UZS',
            'distance_km',
            'weight',
            'volume',
            'length',
            'width',
            'height',
        ]

    def get_distance_km(self, obj):
        return obj.distance_in_km

    def create(self, validated_data):
        length = validated_data.get('length', 0)
        width = validated_data.get('width', 0)
        height = validated_data.get('height', 0)
        validated_data['volume'] = length * width * height
        return AddCargo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        length = validated_data.get('length', instance.length)
        width = validated_data.get('width', instance.width)
        height = validated_data.get('height', instance.height)
        validated_data['volume'] = length * width * height
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LocationInputSerializer(serializers.Serializer):
    loading_location = serializers.CharField(max_length=255)
    unloading_location = serializers.CharField(max_length=255)
    volume = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    distance_in_km = serializers.SerializerMethodField()

    class Meta:
        model = AddCargo
        fields = [
            'loading_location',
            'unloading_location',
            'volume',
            'distance_in_km',
        ]

    def get_distance_in_km(self, obj):
        return obj.distance_in_km


class OrderCarrierSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    loading = serializers.ChoiceField(choices=Loading_choice, required=False)
    volume = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    bid_currency = serializers.CharField(max_length=10, required=False)
    bid_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    price_in_UZS = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    GPS_monitoring = serializers.BooleanField(required=False)

    class Meta:
        model = DeliveryForDrivers
        fields = [
            'contact',
            'loading',
            'volume',
            'bid_currency',
            'bid_price',
            'price_in_UZS',
            'GPS_monitoring',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
