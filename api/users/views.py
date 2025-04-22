from django.contrib.admin import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action  # Correct import

from api.users.models import User
from api.users.serializers import UserSerializer, UserCreateSerializer


class UserListCreateView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(query_serializer=UserSerializer)
    @action(detail=False, methods=['get'], url_path='get-users')
    def get_users(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(query_serializer=UserCreateSerializer)
    @action(detail=False, methods=['post'], url_path='create-user')
    def create_user(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
