from . import consumers
from django.urls import path


websocket_urlpatterns=[
    
   path('ws/chat/<str:user_id>/',consumers.MyAsyncWebsocketConsumer.as_asgi()),

]