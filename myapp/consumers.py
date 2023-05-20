
from channels.generic.websocket import AsyncWebsocketConsumer


class HelloConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        response = f"Привет, {text_data}"
        await self.send(response)



from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Присоединение к группе "notifications"
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от группы "notifications"
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def notify_new_user(self, event):
        await self.send(text="Новый пользователь зарегистрирован!")
