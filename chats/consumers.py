from .models import Message,Chat


from django.db.models import Q
from django.contrib.auth import get_user_model


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


import json



class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    """ 
    For Chatting System Between Seller-Buyer
    """

    async def connect(self):
        self.user = self.scope['user']
        # ! Gets the user model from route
        self.receiver= await database_sync_to_async(get_user_model().objects.get)(id=self.scope['url_route']['kwargs']['user_id'])

        # ! Checks whose user.id is greater for setting a group name
        if self.user.id > self.receiver.id:
            self.room_group_name = f"{self.user.id}{self.receiver.id}"
        else:
            self.room_group_name = f"{self.receiver.id}{self.user.id}"

        #    ! Add them to a group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # ! For accepting a connection
        await self.accept()



# ! Runs when a websocket receives a message
    async def receive(self, text_data=None, bytes_data=None):
  
        # ! Loads the json data received into python object
        data=json.loads(text_data)
        message=data['msg']

        # ! Tries to Find chat object for the related users 
        chat=await database_sync_to_async(Chat.objects.filter(
        Q(initiator=self.user,receiver=self.receiver) |  Q(initiator=self.receiver,receiver=self.user)
        ).first)()

        # ! If chat object does'nt exists it creates one 
        if not chat:
            chat= await database_sync_to_async(Chat.objects.create)(initiator=self.user,receiver=self.receiver)
        
        # ! Creates a message object in the chat  and saves the received message it to db 
        msg_object=await database_sync_to_async(Message.objects.create)(sender=self.user, content=message,chat=chat)
        msg_sender=msg_object.sender

        # ! For sending the received method to client end but calling type casting function
        # ! with like a context message and sender
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat.message',
                'message':message,
                'sender':str(msg_sender)
            }
        )

    
    # ! Chat message function
    async def chat_message(self,event):
 
        #  ! send the message and the message sender to client end 
        await self.send(text_data=json.dumps({
            "msg":event['message'],
            'sender':event['sender']
            }))



# ! For disconnecting a websocket 
    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            )