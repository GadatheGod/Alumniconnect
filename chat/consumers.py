import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from alumni.models import AlumniProfile

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        try:
            room = await self.get_room()
            if not room:
                await self.close()
                return

            user = self.scope['user']
            if not user.is_authenticated or user not in room.members.all():
                await self.close()
                return

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

        except Exception:
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception:
            pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', '')

        if message_type == 'send_message':
            content = data.get('content', '').strip()
            if content and len(content) <= 5000:
                message = await self.save_message(
                    room_id=self.room_id,
                    sender=self.scope['user'],
                    content=content
                )
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message_id': message.id,
                        'sender_id': message.sender.id,
                        'sender_name': await self.get_sender_name(message.sender),
                        'content': message.content,
                        'timestamp': message.created_at.isoformat(),
                        'is_read': False,
                    }
                )

    async def chat_message(self, data):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message_id': data['message_id'],
            'sender_id': data['sender_id'],
            'sender_name': data['sender_name'],
            'content': data['content'],
            'timestamp': data['timestamp'],
            'is_read': data['is_read'],
        }))

    @database_sync_to_async
    def get_room(self):
        try:
            return ChatRoom.objects.get(id=self.room_id)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, room, sender, content):
        return Message.objects.create(room=room, sender=sender, content=content)

    @database_sync_to_async
    def get_sender_name(self, user):
        try:
            profile = user.alumni_profile
            return profile.full_name or user.get_full_name()
        except AlumniProfile.DoesNotExist:
            return user.get_full_name() or user.username
