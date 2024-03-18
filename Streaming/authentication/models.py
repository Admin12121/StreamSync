from django.contrib.auth.models import User
from django.db import models
from moviepy.editor import VideoFileClip
# Create your models here.

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    description = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.title}"