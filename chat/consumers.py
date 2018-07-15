# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import * 
from channels.db import database_sync_to_async
import logging
from django.core import serializers

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous == True:
            raise Exception()
        room_id = self.scope['url_route']['kwargs']['room_name']
        room = await self.get_room(room_id)
        users = await self.get_user_set(room) 
        user = await self.get_user_in_room(room,users)
        self.room_group_name = 'chat_%s' % room_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_id = self.scope['url_route']['kwargs']['room_name']
        room = await self.get_room(room_id)
        users = await self.get_user_set(room) 
        user = await self.get_user_in_room(room,users)
        await self.add_message_to_room_user(room,user,message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_room(self,room_id):
        return Room.objects.get(id=room_id)

    @database_sync_to_async
    def get_user_set(self, room):
        return room.user.all()

    @database_sync_to_async
    def get_user_in_room(self, room, users):
        return users.get(username=self.user.username)
 
    @database_sync_to_async
    def add_message_to_room_user(self,room,user,txt):
        Message.objects.create(room=room, user=user, text=txt)
        