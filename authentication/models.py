from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# Create your models here.

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    description = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    views =  models.IntegerField( default=0)
    likes =  models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.title}"
    


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=5000)

    def __str__(self):
        return f"Comment by {self.video.title}"
    
class LiveStream(models.Model):
    title = models.TextField(max_length=500 , blank=True, null=True)
    url = models.URLField(max_length=1000,blank=True, null=True)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

class News(models.Model):
    title = models.CharField(max_length=500 , blank=True, null=True)
    url = models.URLField(max_length=1000,blank=True, null=True)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    title1 = models.CharField(max_length=500 , blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    article = models.TextField(max_length=5000, blank=True, null=True)
    title2 = models.CharField(max_length=500 , blank=True, null=True)
    image1 = models.ImageField(upload_to='images/', blank=True, null=True)
    article2 = models.TextField(max_length=5000, blank=True, null=True)
    title3 = models.CharField(max_length=500 , blank=True, null=True)
    image2 = models.ImageField(upload_to='images/', blank=True, null=True)
    article3 = models.TextField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

class Events(models.Model):
    event = models.TextField(max_length=500 , blank=True, null=True)
    url = models.URLField(max_length=1000,blank=True, null=True)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.event}"

class Contact(models.Model):
    fname =  models.CharField(max_length=100, blank=True, null=True)
    lname =  models.CharField(max_length=100, blank=True, null=True)
    email =  models.CharField(max_length=100, blank=True, null=True)
    message =  models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.fname} - {self.email}"

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile = models.ImageField(upload_to='profile/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True,default="")
    country = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email
    
@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(
            user=instance,
            profile="",
            bio="",
            country="",
            address=""
        )
