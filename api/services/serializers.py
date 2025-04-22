from rest_framework import serializers
from api.services.models import ServicesModel


class ServicesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesModel
        fields = ['id', 'name', 'descriptions', 'is_active', 'created_at', 'updated_at']
