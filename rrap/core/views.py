import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.contrib import messages
from rrap.users.decorators import onboarding_required
from rrap.organizations.decorators import member_required, main_owner_required
from rrap.datasets.models import Dataset
from rrap.organizations.models import Organization
from .models import Location, Topic
from rrap.datasets.filters import location_based_filter, dataset_filter
from hitcount.utils import get_hitcount_model
from hitcount.views import _update_hit_count


# @login_required
# @onboarding_required
def home(request):

    verified = False

    if request.user.is_authenticated:

        # first check if user is not staff and has whether has finished registration via onboarding
        if (
            not request.user.is_staff
            and not request.user.profile.has_finished_registration
        ):
            return redirect("users:onboarding")

        # if request.user.is_staff:
        #     return redirect("/cms")

        # Check if user has verified email
        verified = ""
        if EmailAddress.objects.filter(user=request.user, verified=True).exists():
            pass
        else:
            verified = False
            messages.warning(
                request,
                "We sent a verification link to your email account. Please click the link to fully activate your account.",
            )

    context = {
        "verified": verified,
    }

    return render(request, "core/home.html", context)


def datasets(request):
    datasets = dataset_filter(request)
    organizations = Organization.objects.all().order_by("title")
    locations = Location.objects.all().order_by("name")
    topics = Topic.objects.all().order_by("name")

    context = {
        "datasets": datasets,
        "organizations": organizations,
        "locations": locations,
        "topics": topics,
    }

    return render(request, "core/datasets.html", context)


def organizations(request):
    organizations = Organization.objects.all()

    context = {"organizations": organizations}

    return render(request, "core/organizations.html", context)


def locations(request):
    # get district list
    locations = Location.objects.all().order_by("name")
    try:
        # Get all valid projects i.e those that have been assigned districts.
        datasets = Dataset.objects.exclude(locations=None)
        if datasets:
            # we need the ids of all the valid projects first
            datasets_ids = datasets.values_list("id", flat=True)
            # then we use the ids to get a query of all the districts chosen
            locations_involved = Location.objects.filter(datasets__in=datasets_ids)
            # get the geojson of all these districts to be used to render on map.
            all_locations = serialize(
                "geojson",
                locations_involved,
                geometry_field="geom",
                fields=("pk", "name", "population"),
            )
            # load the json for modification
            locations_json = json.loads(all_locations)
            if locations_json:
                # add id field to features
                i = 0
                for p in locations_json["features"]:
                    i += 1
                    p["id"] = i
                # remove crs element. It confuses mapbox
                locations_json.pop("crs", None)
                # restore the clean json
                locations_json = json.dumps(locations_json)
            else:
                locations_json = ""
    except Dataset.DoesNotExist:
        raise NotImplementedError

    return render(
        request,
        "core/locations.html",
        {
            "datasets": datasets,
            "locations": locations,
            "locations_json": locations_json,
            "mapbox_access_token": settings.MAPBOX_ACCESS_TOKEN,
        },
    )


def location(request, location_pk):
    location = get_object_or_404(Location, pk=location_pk)
    datasets = location_based_filter(request, location.pk)
    organizations = location.organizations.all()
    return render(
        request,
        "core/location.html",
        {
            "location": location,
            "datasets": datasets,
            "organizations": organizations,
        },
    )


def dataset(request, dataset_uuid):
    dataset = get_object_or_404(Dataset, uuid=dataset_uuid)
    context = {}
    # hit count
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(dataset)
    hits = hit_count.hits
    hitcontext = context["hitcount"] = {"pk": hit_count.pk}
    hit_count_response = _update_hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext["hit_counted"] = hit_count_response.hit_counted
        hitcontext["hit_message"] = hit_count_response.hit_message
        hitcontext["total_hits"] = hits

    return render(
        request,
        "core/dataset.html",
        {"dataset": dataset},
    )


def organization(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)
    datasets = organization.get_published_datasets()
    locations = Location.objects.all()
    followers = organization.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = organization.get_followers_count()

    return render(
        request,
        "organizations/single/data.html",
        {
            "organization": organization,
            "datasets": datasets,
            "locations": locations,
            "is_following": is_following,
            "follower_count": followers_count,
        },
    )


@member_required
@login_required
def draft_datasets(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)
    datasets = organization.get_draft_datasets()
    locations = Location.objects.all()
    followers = organization.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = organization.get_followers_count()

    return render(
        request,
        "organizations/single/draft_data.html",
        {
            "organization": organization,
            "datasets": datasets,
            "locations": locations,
            "is_following": is_following,
            "follower_count": followers_count,
        },
    )


def organization_activity(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)
    activity = {}
    followers = organization.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = organization.get_followers_count()

    return render(
        request,
        "organizations/single/activity.html",
        {
            "organization": organization,
            "activity": activity,
            "is_following": is_following,
            "follower_count": followers_count,
        },
    )


@member_required
@login_required
def organization_members(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)
    members = {}
    followers = organization.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = organization.get_followers_count()

    return render(
        request,
        "organizations/single/members.html",
        {
            "organization": organization,
            "members": members,
            "is_following": is_following,
            "follower_count": followers_count,
        },
    )


def organization_followers(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)
    followers = organization.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = organization.get_followers_count()

    return render(
        request,
        "organizations/single/followers.html",
        {
            "organization": organization,
            "followers": followers,
            "is_following": is_following,
            "follower_count": followers_count,
        },
    )
