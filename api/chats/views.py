from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from ..base.paginator import CustomPagination


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'], url_path='get-chats')
    def get_chats(self, request):
        if request.user.is_staff:
            chats = Chat.objects.all()
        else:
            chats = Chat.objects.filter(participants=request.user)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(chats, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=ChatSerializer)
    @action(detail=False, methods=['post'], url_path='create-chat')
    def create_chat(self, request):
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        participants = validated_data.pop('participants')
        chat = Chat.objects.create()
        chat.participants.set(participants)
        chat.save()

        response_serializer = ChatSerializer(chat)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'], url_path='get-messages')
    def get_messages(self, request):
        if request.user.is_staff:
            messages = Message.objects.all()
        else:
            messages = Message.objects.filter(chat__participants=request.user)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(messages, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=MessageSerializer)
    @action(detail=False, methods=['post'], url_path='send-message')
    def send_message(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        chat = validated_data.get('chat')
        content = validated_data.get('content')

        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        if not chat.participants.filter(id=user.id).exists():
            return Response({"error": "User is not a participant of the chat"}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(chat=chat, content=content, sender=user)
        response_serializer = MessageSerializer(message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
