from django.urls import path
from . import consumers


websocket_urlpatterns=[
   path('ws/ayush/',consumers.MySyncWebsocketConsumer.as_asgi()),

]