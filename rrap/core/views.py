from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.contrib import messages
from rrap.users.decorators import onboarding_required
from rrap.datasets.models import Dataset
from rrap.organizations.models import Organization
from .models import Location


@login_required()
@onboarding_required()
def home(request):
    profile = request.user.profile

    # first check if user is not staff and has whether has finished registration via onboarding
    if not request.user.is_staff and not request.user.profile.has_finished_registration:
        return redirect("users:onboarding")

    if request.user.is_staff:
        return redirect("/admin")

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
        "profile": profile,
        "verified": verified,
    }

    return render(request, "core/home.html", context)


def datasets(request):
    datasets = Dataset.objects.all()

    context = {"datasets": datasets}

    return render(request, "core/datasets.html", context)


def organizations(request):
    organizations = Organization.objects.all()

    context = {"organizations": organizations}

    return render(request, "core/organizations.html", context)


def locations(request):
    locations = Location.objects.all()

    context = {"locations": locations}

    return render(request, "core/locations.html", context)


def dataset(request, dataset_uuid):
    dataset = get_object_or_404(Dataset, uuid=dataset_uuid)

    return render(
        request,
        "core/dataset.html",
        {
            "dataset": dataset,
        },
    )


def organization(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)

    return render(
        request,
        "core/organization.html",
        {
            "organization": organization,
        },
    )
