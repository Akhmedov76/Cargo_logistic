from rest_framework import serializers

from api.users.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'phone_number', 'email', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    phone_number = serializers.CharField(required=True, help_text="e.g. +998901234567")
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'phone_number', 'email', ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8,
                                     help_text=_("Password must be at least 8 characters long."))
    phone_number = serializers.CharField(required=True, help_text="e.g. +998901234567")

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email is already registered."))
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(_("Phone number is already registered."))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'message': _('User matching query does not exist')}
            )
        return attrs
