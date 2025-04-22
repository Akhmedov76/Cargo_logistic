from django.contrib.admin import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action  # Correct import
from django.contrib.auth import authenticate

from api.users.models import User
from api.users.serializers import UserSerializer, UserCreateSerializer, RegisterSerializer, LoginSerializer


class UserListCreateView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(query_serializer=UserSerializer)
    @action(detail=False, methods=['get'], url_path='get-users')
    def get_users(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email'],
                phone_number=serializer.validated_data['phone_number'],
                role=serializer.validated_data['role'],
                company=serializer.validated_data['company']
            )
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""{
  "username": "jastin",
  "password": "74108520Jas",
  "email": "jas@example.com",
  "phone_number": "+999815112",
  "role": "operator"
}"""
