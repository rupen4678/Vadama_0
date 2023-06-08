from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
import json

User = get_user_model()

#for now causing the lazyzinesss and server load because of variable receiver
class UserChat(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f"chat_{self.room_name}"
        receiver_username, sender_username = str(self.room_name).split('_')

        self.sender = await self.get_user(sender_username)
        self.receiver = await self.get_user(receiver_username)
        self.chat_room = await self.get_or_create_chat_room(self.sender, self.receiver)
        await self.add_receiver_to_chat_room(self.chat_room, self.receiver, self.sender)

        self.room_name = str(self.chat_room.id)
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send the initial data to the client
        # await self.send_initial_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_json = json.loads(text_data)
        msgtype = text_json['type']

        if msgtype == 'get_initial_data':
            await self.send_initial_data()
            # data = await self.get_user_list(self.scope['user'])
            # data = serializers.serialize('json', data)
            # await self.send(text_data=json.dumps(data))
        
        elif msgtype == "initial_data":
            receiver = text_json['receiver']
            await self.send_chat(receiver)    
            
        #this will handle both chat addition
        elif msgtype == 'pvt_msg':
            print('i am handling ajax call')
            author1 = self.scope['user']
            message = text_json['message']
            rec = text_json['receiver']
            receiver = await self.get_user(rec)
            chat_room = await self.get_or_create_chat_room(self.sender, receiver)
            msg = await self.create_message(chat_room, self.sender, receiver, message, author1)
            author = str(author1.username)

            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': msg.content,
                    'author': author,
                }
            )
        elif msgtype == 'users_list':
            pass

    async def chat_message(self, event):
        messages = event['message']
        author = event['author']
        print(f'chat_message {messages} {author}')

        await self.send(text_data=json.dumps({
            'message': messages,
            'type': 'pvt_msg',
            'author': author,
        }))
        
    async def send_chat(self, receiver):
        print('getting from the ajax')
        receiver_username = await self.get_user(receiver)
        chat_room = await self.get_or_create_chat_room(self.sender, receiver_username)
        messages = await self.get_messages(chat_room)
        authors = await self.get_author(chat_room)
        
        data = {
            'type': 'initial_data',
            'message': messages,
            'author': authors,
        }

        await self.send(text_data=json.dumps(data))
        
    async def send_initial_data(self):        
        print('this is initial data')
        messages = await self.get_messages(self.chat_room)
        authors = await self.get_author(self.chat_room)

        data = {
            'type': 'initial_data',
            'message': messages,
            'author': authors,
        }

        await self.send(text_data=json.dumps(data))

    @staticmethod
    @database_sync_to_async
    def get_user_list(user):

        chat_rooms = ChatRoom.objects.filter(members=user)
        user_ids = []
        for chat_room in chat_rooms:
            user_ids.extend(chat_room.members.all().values_list('id', flat=True))

        # Retrieve the usernames of the users in the chat rooms
        users = User.objects.filter(id__in=user_ids)
        user_list = [{'id': user.id, 'username': user.username} for user in users]
        data = {
            'type': 'users_list',
            'users': user_list
        }
        return data

    @staticmethod
    @database_sync_to_async
    def get_user(username):
        return User.objects.get(username=username)

    @staticmethod
    @database_sync_to_async
    def get_or_create_chat_room(sender, receiver):
        sender_username = sender
        receiver_username = receiver
        chat_rooms = ChatRoom.objects.filter(
            members__username=receiver_username).filter(members__username=sender_username)

        if chat_rooms.exists():
            chat_room = chat_rooms.first()
        else:
            chat_room = ChatRoom.objects.create()
            chat_room.members.add(receiver_username, sender_username)
        return chat_room

    @staticmethod
    @database_sync_to_async
    def add_receiver_to_chat_room(chat_room, receiver, sender):
        chat_room.members.add(receiver)
        chat_room.members.add(sender)

    @staticmethod
    @database_sync_to_async
    def create_message(chat_room, sender, receiver, content, author):
        return Message.objects.create(room=chat_room, content=content, author=author)

    @staticmethod
    @database_sync_to_async
    def get_messages(chat_room):
        messages = Message.objects.filter(room=chat_room)
        return [message.content for message in messages]

    @staticmethod
    @database_sync_to_async
    def get_author(chat_room):
        authors = Message.objects.filter(room=chat_room)
        return [author.author.username for author in authors]
