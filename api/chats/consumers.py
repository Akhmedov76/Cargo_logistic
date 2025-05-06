import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            sender_id = self.scope["user"].id
            if not self.scope["user"].is_authenticated:
                print("⚠️ Foydalanuvchi autentifikatsiyadan o‘tmagan!")
                return

            await self.save_message(self.chat_id, sender_id, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                }
            )
        except json.JSONDecodeError:
            print("❌ Noto‘g‘ri JSON format!")
        except KeyError:
            print("❌ 'message' kaliti topilmadi.")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
        }))

    @database_sync_to_async
    def save_message(self, chat_id, sender_id, message):
        chat = Chat.objects.get(id=chat_id)
        sender = User.objects.get(id=sender_id)
        return Message.objects.create(chat=chat, sender=sender, content=message)
