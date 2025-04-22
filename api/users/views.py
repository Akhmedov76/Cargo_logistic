from django.contrib.admin import action
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.translation import gettext_lazy as _
from api.users.models import User
from api.users.serializers import UserSerializer, UserCreateSerializer, RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        if get_user_model().objects.filter(email=email).exists():
            return Response(
                {"message": _("User exists with this email. Please enter another email address.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response({"message": _("Registration successful!")}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": _("User does not exist")}, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password) and user.is_active:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            login(request, user)
            return Response({"message": _("Login successful!")}, status=status.HTTP_200_OK)

        return Response({"error": _("Invalid email or password")}, status=status.HTTP_401_UNAUTHORIZED)


class UserListCreateView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(query_serializer=UserSerializer)
    @action(detail=False, methods=['get'], url_path='get-users')
    def get_users(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
