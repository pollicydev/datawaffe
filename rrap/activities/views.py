import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext

from rrap.organizations.models import OrganisationPage

from .constants import ActivityTypes
from .models import Activity

logger = logging.getLogger(__name__)

User = get_user_model()


@login_required
def follow(request, org_slug):
    try:
        organisation = get_object_or_404(OrganisationPage, slug=org_slug)
        from_user = request.user

        following = from_user.profile.get_following()

        if organisation not in following:
            Activity.objects.create(
                from_user=from_user,
                organisation=organisation,
                activity_type=ActivityTypes.FOLLOW,
            )
            context = {"organisation": organisation}
            return render(request, "partials/unfollow.html", context)
        else:
            return HttpResponseBadRequest()
    except Exception:
        logger.exception("An error occurred while trying to follow the organisation.")
        return HttpResponseBadRequest()


@login_required
def unfollow(request, org_slug):
    try:
        organisation = get_object_or_404(OrganisationPage, slug=org_slug)
        from_user = request.user

        following = from_user.profile.get_following()

        if organisation in following:
            Activity.objects.filter(
                from_user=from_user,
                organisation=organisation,
                activity_type=ActivityTypes.FOLLOW,
            ).delete()
            context = {"organisation": organisation}
            return render(request, "partials/follow.html", context)
        else:
            return HttpResponseBadRequest()
    except Exception:
        logger.exception("An error occurred while trying to unfollow the organisation.")
        return HttpResponseBadRequest()


def update_followers_count(request, org_slug):
    try:
        organisation = get_object_or_404(OrganisationPage, slug=org_slug)
        followers_count = organisation.get_followers_count()
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
    organization = get_object_or_404(OrganisationPage, name=org_name)
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
