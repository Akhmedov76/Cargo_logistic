import json
import os
import sys
from datetime import timezone

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import close_old_connections

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


class ServiceExcelFileConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        self.user_room_name = "room_" + str(self.user['user_id'])
        print(self.user_room_name)
        await self.channel_layer.group_add(self.user_room_name, self.channel_name)
        print(f"Added chat {self.channel_name}")
        now = timezone.now()
        two_hours_ago = now - timezone.timedelta(hours=2)
        try:
            close_old_connections()  # Ulanishni yangilang
            data = await sync_to_async(lambda: list(
                ServiceExcelFile.objects.filter(status=0, is_down=False, updated__gte=two_hours_ago).values('id',
                                                                                                            'request_received_count',
                                                                                                            'request_all_count')))()

            res_data = []
            for i in data:
                if i['request_all_count'] != 0:
                    percentage = i['request_received_count'] * 100 / i['request_all_count']
                else:
                    percentage = 0
                res_data.append({'id': i['id'], 'percentage': percentage})

            await self.send(text_data=json.dumps({
                "message": res_data
            }))
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    async def disconnect(self, event):
        self.user = self.scope["user"]
        self.user_room_name = "room_" + str(self.user['user_id'])
        print(self.user_room_name)
        await self.channel_layer.group_discard(self.user_room_name, self.channel_name)
        print(f"Removed chat {self.channel_name}")

    async def new_message(self, event):
        await self.send_json(event)
        print(f"Got messages chat {event} at {self.channel_name}")

    async def new_notification(self, event):
        await self.send_json(event)
        print(f"Got messages {event} at {self.channel_name}")
