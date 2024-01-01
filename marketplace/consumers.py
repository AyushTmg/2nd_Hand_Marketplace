from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import Message



class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.other_user = await database_sync_to_async(get_user_model().objects.get)(pk=self.scope['url_route']['kwargs']['pk'])
        self.room_name = f"{self.user.username}_{self.other_user.username}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print(f"Message receiced from client {text_data}")
        print(type(text_data))
        data=json.loads(text_data)
        message=data['msg']
        await database_sync_to_async(Message.objects.create)(sender=self.user, receiver=self.other_user, content=message)
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat.message',
                'message':message
            }
        )

    async def chat_message(self,event):
        print(event)
        await self.send(text_data=json.dumps({
            "msg":event['message']
            }))

        

    async def disconnect(self, code):
        print(code)