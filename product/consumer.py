import json 
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core import serializers
from random import random

from home.models import Comments, Like, Profile, add_product, sub_comment

class ProductConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.group = 'noti1'

        await self.channel_layer.group_add(
            self.group,
            self.channel_name,
        )
        await self.accept()

        id2 = int(self.scope['url_route']['kwargs']['pk'])

        @sync_to_async
        def get_comments(id1):
            commenta = Comments.objects.filter(post=add_product.objects.get(id=id1))
            suma = serializers.serialize('json', commenta)
            return suma

        comments = await get_comments(id2)

        # Send the existing comments to the client
        await self.send(text_data=json.dumps({
            'type': 'comm',
            'message': comments,
        }))
        print(f'data was sent after connection + {self.scope["user"]}')

    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )
    
    async def receive(self, text_data):
        print('inside the receive data function')
        text_json = json.loads(text_data)
        message = text_json['message']
        print('message being received {}'.format(message))
        productid = text_json['product_id']
        user = self.scope['user']

        print(f'see the username i get {user}')
        await self.channel_layer.group_send(
            self.group, {"type": "update_info", "message": message, 'productid': productid, 'user': user.username},
        )

    async def update_info(self, event):
        print('running update_info')
        comment = event['message']
        productid = event['productid']
        user = self.scope['user']
        
        try:
            @sync_to_async
            def save_comments():
                com1 = Comments(
                    post=add_product.objects.get(id=productid),
                    username=user,
                    man=user,
                    comment=comment,
                )
                com1.save()
                print(f'Saving comment: productid={productid}, user={user}, comment={comment}')

            await save_comments()

        except Exception as e:
            print(f'problem saving the database: {e}')
        
        #comments = Comments.objects.filter(post=add_product.objects.get(id=productid))
        @sync_to_async
        def get_comments(id1):
            commenta = Comments.objects.filter(post=add_product.objects.get(id=id1))
            suma = serializers.serialize('json', commenta)
            return suma

        commentx = await get_comments(productid)
            
        await self.send(text_data=json.dumps({
            'type': 'comm',
            'message': commentx,
        }))
        print('data sent from update info after saving it')

