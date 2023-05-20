from django.urls import re_path
from myapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/hello/$', consumers.HelloConsumer.as_asgi()),
]
