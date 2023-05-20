
from channels.generic.websocket import AsyncWebsocketConsumer


class HelloConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        response = f"Привет, {text_data}"
        await self.send(response)



from channels.generic.websocket import AsyncWebsocketConsumer

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from myapp.models import Order

channel_layer = get_channel_layer()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Присоединение к группе "notifications"
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от группы "notifications"
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def notify_new_order(self, event):
        order_id = event['order_id']
        message = f"Новый заказ создан! ID: {order_id}"
        await self.send(text_data=message)

