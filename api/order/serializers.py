from random import choices

from rest_framework import serializers

from api.country.models import District
from api.order.models import AddCargo, DeliveryForDrivers
from api.users.models import User


class OrderCargoSerializer(serializers.ModelSerializer):
    cargo = serializers.SlugRelatedField(read_only=True, slug_field='name')
    services = serializers.SlugRelatedField(read_only=True, slug_field='name')
    loading = serializers.SlugRelatedField(read_only=True, slug_field='name')
    unloading = serializers.SlugRelatedField(read_only=True, slug_field='name')
    contact = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = AddCargo
        fields = [
            'id',
            'cargo',
            'weight',
            'length',
            'width',
            'height',
            'volume',
            'when',
            'loading',
            'unloading',
            'services',
            'contact',
            'GPS_monitoring',
            'bid_currency',
            'bid_price',
            'price_in_UZS', ]

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


class OrderCarrierSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    loading = serializers.ChoiceField(choices=DeliveryForDrivers.Loading_choice, required=False)
    body_volume = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    where = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)
    where_to = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)
    bid_currency = serializers.CharField(required=False, max_length=10)
    bid_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    price_in_UZS = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    GPS_monitoring = serializers.BooleanField(required=False)

    class Meta:
        model = DeliveryForDrivers
        fields = [
            'contact',
            'loading',
            'body_volume',
            'where',
            'where_to',
            'bid_currency',
            'bid_price',
            'price_in_UZS',
            'GPS_monitoring',
        ]

    def create(self, validated_data):
        instance = DeliveryForDrivers.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
