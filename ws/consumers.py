import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

class HelloConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        response = f"Привет, {text_data}"
        await self.send(response)



class YourConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        await self.send({
            "type": "websocket.send",
            "text": "Hello from Django socket"
        })

    async def websocket_disconnect(self, event):
        pass

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Выполните необходимую аутентификацию или авторизацию пользователя

        # Подключите пользователя к группе WebSocket
        await self.channel_layer.group_add('notifications', self.channel_name)

        # Принимаем соединение WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Отключите пользователя от группы WebSocket
        await self.channel_layer.group_discard('notifications', self.channel_name)

    async def receive(self, text_data):
        # Парсинг текстового сообщения
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Ваша логика обработки сообщения
        # ...

        # Отправка ответного сообщения
        response = {
            'status': 'success',
            'message': 'Message received and processed successfully',
        }
        await self.send(text_data=json.dumps(response))

    async def notify_new_user(self, event):
        # Отправка уведомления о новом пользователе через WebSocket
        await self.send(text_data=event['message'])
