from django.contrib.auth.models import User
from django.db import models
from moviepy.editor import VideoFileClip
# Create your models here.

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    description = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.videourl:
            clip = VideoFileClip(self.videourl)
            duration_in_seconds = clip.duration
            self.duration_minutes = int(duration_in_seconds // 60)
            self.duration_seconds = int(duration_in_seconds % 60)
            super().save(*args, **kwargs)
    def __str__(self):
        return self.name