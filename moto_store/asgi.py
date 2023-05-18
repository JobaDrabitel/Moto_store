import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from ws.routing import websocket_urlpatterns as ws_websocket_urlpatterns, websocket_urlpatterns
application = get_asgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moto_store.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(websocket_urlpatterns + ws_websocket_urlpatterns),
})
