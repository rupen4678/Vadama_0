from django.shortcuts import render
from home.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from django.db.models import Q
import uuid 
import random
from django.contrib.auth.models import User
from django.http import JsonResponse



@login_required
def UsersChat(request, pk):
    receiver_username, sender_username = pk.split('_')
    
    chat_room = ChatRoom.objects.filter(
        Q(members__username=receiver_username) & Q(members__username=sender_username)
    ).first()
    
    if chat_room is None:
        chat_room = ChatRoom.objects.create()
        receiver = User.objects.get(username=receiver_username)
        sender = User.objects.get(username=sender_username)
        chat_room.members.add(receiver, sender)
    
    msg = []
    if chat_room is not None:
        msg.append(f"created chat {chat_room}")
    else: 
        msg.append(f"i think there is problem with {chat_room}")
        
    # Get the other user
    other_users = chat_room.members.exclude(id=request.user.id)
    print(f'the other user{other_users}')
    if other_users.exists():
        other_user = other_users.first()
        print(f'the other user is {other_user}')
    else:
        other_user = None
        
    profile_image, done = Profile.objects.get_or_create(user=request.user)
    avatar = profile_image.avatar.url
    if done:
        msg.append(f'done creating the profile')
    else:
        msg.append(f'problem or already profile creation')
        
    cuser = request.user
    users = get_user_list(request)
    
    return render(request, 'chatting/index1.html',{
        "avatar" : avatar,
        "msg": msg,
        "cuser" : cuser,
        'users' : users,
    })
    
def get_user_list(request):
    # Retrieve the chat rooms where the current user is a member
    chat_rooms = ChatRoom.objects.filter(members=request.user)
    user_ids = []
    for chat_room in chat_rooms:
        user_ids.extend(chat_room.members.values_list('id', flat=True))

    # Retrieve the usernames of the users in the chat rooms
    users = User.objects.filter(id__in=user_ids)
    user_list = [{'id': user.id, 'username': user.username} for user in users]

    #refining the list so it dosent include the current user 
    the_user = str(request.user)
    final_list = [i['username'] for i in user_list if 'username' in i.keys() and the_user not in i['username']]
    print(f'see the final list {final_list}')
    return final_list

def get_users_chat(request):
    if request.method == 'GET':
        users = request.GET['data']
        print(f'see ajax {users}')
    return JsonResponse(data={'data': users})