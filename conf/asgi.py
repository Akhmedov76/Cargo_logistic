# asgi.py
import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import api.chats.routing

application = ProtocolTypeRouter({
    'http': get_default_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            api.chats.routing.websocket_urlpatterns
        )
    ),
})
