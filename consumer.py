import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from random import random
from home.models import Like, add_product
from django.core import serializers


class HomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]
        self.room_group_name = "chat"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_json = json.loads(text_data)
        message = text_json['message']
        productid = text_json['product_id']
        user = self.scope['user']
        
        print(f'showing the data sent from frontend is := {message}')

        await self.update_info(message, productid, user)
        async def update_info(self, message, productId, user):
            comment = message
            productid = productId
            user = user

            try:
                @database_sync_to_async
                def save_comments():
                    print(f'saving comment')
                    com1 = Comments(
                        post=add_product.objects.get(id=productid),
                        username = user,
                        comment = comment,
                    )
                    com1.save()
                await save_comments()

            except Exception as e:
                print(f'problem saving the database{e}')

            @database_sync_to_async
            def get_comments(id1):
                commenta = Comments.objects.filter(post=add_product.objects.get(id=id1))
                suma = serializers.serialize('json', commenta)
                return suma
            commentx = await get_comments(productid)

            await self.send(text_data=json.dumps({
                'type' : 'comm',
                'message' : commentx,
            }))
            print('data sent from updatw info after saving it')