import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Organization, generate_logo


@receiver(pre_save, sender=Organization)
def check_logo_exists(sender, instance, **kwargs):
    if not instance.logo:
        instance.logo = generate_logo(instance)


@receiver(post_save, sender=Organization)
def create_organization(sender, instance, created, **kwargs):
    if created:
        instance.logo = generate_logo(instance)
