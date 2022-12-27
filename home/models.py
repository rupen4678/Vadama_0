from django.db import models
from django.contrib.auth.models import User 
from PIL import Image

class add_product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Image/')
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class sub_comment(models.Model):
    scomment = models.CharField(max_length=255)


class Comments(models.Model):
    post = models.ForeignKey(add_product, related_name='details', on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(auto_now_add=True)
    subcomments = models.ForeignKey(sub_comment, related_name='subcomment', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.post.name


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(add_product, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return self.post.name

###################################------------------##########################

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
            
    
    

