from django import template
from django.contrib.auth import get_user_model
from .. import utils

User = get_user_model()

register = template.Library()


@register.simple_tag
def gravatar(user=None, user_uid=None, size=80):
    hasattr(user, "profile")
    if user_uid and hasattr(user, "profile"):
        user = User.objects.filter(profile__uid=user_uid).first()

    return utils.gravatar(user=user, size=size)
