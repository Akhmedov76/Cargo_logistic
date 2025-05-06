from rest_framework import serializers

from api.users.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'phone_number', 'email', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    phone_number = serializers.CharField(required=True, help_text="e.g. +998901234567")
    email = serializers.EmailField(required=True)
    passport_serial = serializers.CharField(required=True)
    passport_number = serializers.CharField(required=True)
    date_given = serializers.DateField(required=True)
    given_by_whom = serializers.CharField(required=True)
    passport_file = serializers.FileField(required=False)
    drivers_license_serial_number = serializers.CharField(required=True)
    date_of_issue_license = serializers.DateField(required=True)
    drivers_license_file = serializers.FileField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'phone_number', 'email', 'passport_serial', 'passport_number',
                  'date_given', 'given_by_whom', 'passport_file', 'drivers_license_serial_number',
                  'date_of_issue_license', 'drivers_license_file']

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
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'role']

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
