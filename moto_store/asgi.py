
from ws.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from django.core.asgi import get_asgi_application
from django.urls import path


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moto_store.settings')

from ws.consumers import YourConsumer


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws', YourConsumer.as_asgi())
        ])
    )
})


application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter(websocket_urlpatterns),
    }
)
