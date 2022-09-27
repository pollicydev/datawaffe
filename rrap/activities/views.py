import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext

from rrap.organizations.models import Organization

from .constants import ActivityTypes
from .models import Activity

logger = logging.getLogger(__name__)

User = get_user_model()


@login_required
def follow(request):
    try:
        org_id = request.GET["organization-id"]
        organization = get_object_or_404(Organization, pk=org_id)
        from_user = request.user

        following = from_user.profile.get_following()

        if organization not in following:
            Activity.objects.create(
                from_user=from_user,
                organization=organization,
                activity_type=ActivityTypes.FOLLOW,
            )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    except Exception:
        logger.exception("An error occurred while trying to follow organization.")
        return HttpResponseBadRequest()


@login_required
def unfollow(request):
    try:
        org_id = request.GET["organization-id"]
        organization = get_object_or_404(Organization, pk=org_id)
        from_user = request.user

        following = from_user.profile.get_following()

        if organization in following:
            Activity.objects.filter(
                from_user=from_user,
                organization=organization,
                activity_type=ActivityTypes.FOLLOW,
            ).delete()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    except Exception:
        logger.exception("An error occurred while trying to unfollow organization.")
        return HttpResponseBadRequest()


def update_followers_count(request):
    try:
        org_id = request.GET["organization-id"]
        organization = get_object_or_404(Organization, pk=org_id)
        followers_count = organization.get_followers_count()
        return HttpResponse(followers_count)
    except Exception:
        return HttpResponseBadRequest()


def following(request, username):
    page_user = get_object_or_404(User, username=username)
    page_title = gettext("following")
    following = page_user.profile.get_following()
    user_following = None

    if request.user.is_authenticated:
        user_following = request.user.profile.get_following()

    return render(
        request,
        "activities/follow.html",
        {
            "page_user": page_user,
            "page_title": page_title,
            "follow_list": following,
            "user_following": user_following,
        },
    )


def followers(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)
    page_title = gettext("followers")
    followers = organization.get_followers()
    user_following = None

    if request.user.is_authenticated:
        user_following = request.user.profile.get_following()

    return render(
        request,
        "activities/follow.html",
        {
            "organization": organization,
            "page_title": page_title,
            "follow_list": followers,
            "user_following": user_following,
        },
    )
