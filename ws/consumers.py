import json
from channels.generic.websocket import AsyncWebsocketConsumer
from myapp.models import Product

class ProductConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('product_updates', self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('product_updates', self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_product_update(self, event):
        product = event['product']
        message = {
            'type': 'product.update',
            'product': {
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'description': product.description,
                'price': str(product.price),
                'imageurl': product.imageurl,
            },
        }
        await self.send(json.dumps(message))
