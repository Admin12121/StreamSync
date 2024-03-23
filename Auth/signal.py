# your_app_name/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserInfo

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    """
    Signal handler to create UserInfo instance when a new User is created.
    """
    # if created:
    #     UserInfo.objects.create(user=instance)
    if created:
        # Create UserInfo instance
        userinfo = UserInfo.objects.create(user=instance)

        # Set default values for bio and profile fields
        userinfo.bio = ""
        userinfo.profile = "profile/default.jpg"
        userinfo.country = ""  # Set to the path of your default profile image
        userinfo.address = ""  # Set to the path of your default profile image
        userinfo.save()

@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
    """
    Signal handler to save UserInfo instance when User is saved.
    """
    instance.userinfo.save()
