import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Profile, User, generate_avatar
from . import tasks

def get_uuid(limit=32):
    return str(uuid.uuid4())[:limit]

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        profile = instance.profile
        profile.avatar = generate_avatar(profile)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_save, sender=User)
def create_uuid(sender, instance, *args, **kwargs):
    instance.username = instance.username or get_uuid(8)
