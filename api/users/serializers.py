from rest_framework import serializers

from api.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'phone_number', 'email', 'company', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'phone_number', 'email', 'company']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user







