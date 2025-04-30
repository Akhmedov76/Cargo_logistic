from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='get-chats')
    def get_chats(self, request):
        if request.user.is_staff:
            chats = Chat.objects.all()
        else:
            chats = Chat.objects.filter(participants=request.user)

        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='get-messages')
    def get_messages(self, request):
        chat_id = request.query_params.get('chat_id')
        messages = Message.objects.filter(chat_id=chat_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
