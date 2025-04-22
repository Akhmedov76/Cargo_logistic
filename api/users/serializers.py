from rest_framework import serializers

from api.users.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'phone_number', 'email', 'company', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    phone_number = serializers.CharField(required=True, help_text="e.g. +998901234567")
    email = serializers.EmailField(required=True)
    company = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'phone_number', 'email', 'company']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=15, help_text="User's unique username")
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True, help_text="e.g. +998901234567")
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    company = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number', 'role', 'company']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email is already registered."))
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'message': _('User matching query does not exist')}
            )
        return attrs
