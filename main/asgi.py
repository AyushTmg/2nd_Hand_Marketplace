
import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import chats.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":AuthMiddlewareStack(URLRouter(
            chats.routing.websocket_urlpatterns 
    ))
})
