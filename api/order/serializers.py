from rest_framework import serializers
from api.order.models import DeliveryRequest, DeliveryForDrivers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRequest
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryForDrivers
        fields = '__all__'
