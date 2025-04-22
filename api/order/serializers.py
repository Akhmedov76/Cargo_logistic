from random import choices

from rest_framework import serializers

from api.country.models import District
from api.order.models import DeliveryRequest, DeliveryForDrivers
from api.users.models import User


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRequest
        fields = [
            'id',
            'cargo',
            'weight',
            'capacity',
            'when',
            'loading',
            'download',
            'services',
            'role', ]

    def create(self, validated_data):
        return DeliveryRequest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class OrderCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False)
    loading = serializers.ChoiceField(choices=DeliveryForDrivers.Loading_choice, required=False)
    vehicle = serializers.CharField(max_length=55, required=False, allow_blank=True)
    body_volume = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    where = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)
    where_to = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)
    company = serializers.CharField(max_length=55, required=False, allow_blank=True)

    class Meta:
        model = DeliveryForDrivers
        fields = [
            'role',
            'loading',
            'vehicle',
            'body_volume',
            'where',
            'where_to',
            'company',
        ]

    def create(self, validated_data):
        return DeliveryForDrivers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
