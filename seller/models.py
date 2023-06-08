from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    members = models.ManyToManyField(User, related_name='chat_rooms')
    def __str__(self):
        return ', '.join([str(member) for member in self.members.all()])
        
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='messages',default=None)
    created_at = models.DateTimeField(auto_now_add=True)