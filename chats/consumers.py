from .models import Message,Chat


from django.db.models import Q
from django.contrib.auth import get_user_model


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


import json



class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.receiver= await database_sync_to_async(get_user_model().objects.get)(id=self.scope['url_route']['kwargs']['user_id'])


        if self.user.id > self.receiver.id:
            self.room_group_name = f"{self.user.id}{self.receiver.id}"
        else:
            self.room_group_name = f"{self.receiver.id}{self.user.id}"


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):

        data=json.loads(text_data)
        message=data['msg']

        chat=await database_sync_to_async(Chat.objects.filter(
        Q(initiator=self.user,receiver=self.receiver) |  Q(initiator=self.receiver,receiver=self.user)
        ).first)()

        if not chat:
            chat= await database_sync_to_async(Chat.objects.create)(initiator=self.user,receiver=self.receiver)
        
        msg_object=await database_sync_to_async(Message.objects.create)(sender=self.user, content=message,chat=chat)
        msg_sender=msg_object.sender

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat.message',
                'message':message,
                'sender':str(msg_sender)
            }
        )

    async def chat_message(self,event):

        await self.send(text_data=json.dumps({
            "msg":event['message'],
            'sender':event['sender']
            }))



    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            )