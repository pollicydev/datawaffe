import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Organization, generate_logo


@receiver(post_save, sender=Organization)
def create_organization(sender, instance, created, **kwargs):
    if created:
        Organization.objects.create(organization=instance)
        organization = instance.organization
        organization.logo = generate_logo(organization)


@receiver(post_save, sender=Organization)
def save_organization_profile(sender, instance, **kwargs):
    instance.save()
