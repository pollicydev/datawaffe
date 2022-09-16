from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse as r
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from .decorators import member_required, main_owner_required
from .forms import CreateOrganizationForm, OrganizationForm
from .models import Organization
from rrap.invites.constants import InviteStatus
from django.core.paginator import Paginator

User = get_user_model()


@login_required
def organizations(request):
    username = request.user.username
    user = get_object_or_404(User, username__iexact=username)
    organizations = Organization.objects.all().order_by("-create_date")
    user_organizations = user.profile.get_organizations()

    pending_invites = user.invites_received.filter(status=InviteStatus.PENDING)
    pending_invites_count = pending_invites.count()

    paginator = Paginator(organizations, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "organizations/organizations.html",
        {
            "organizations": organizations,
            "page_obj": page_obj,
            "page_number": page_number,
            "user_organizations": user_organizations,
            "page_user": user,
            "pending_invites": pending_invites,
            "pending_invites_count": pending_invites_count,
        },
    )


@login_required
def new(request):
    if request.method == "POST":
        form = CreateOrganizationForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user

            name = slugify(form.instance.title)
            if not name:
                name = "organization"
            unique_name = name
            i = 0
            while Organization.objects.filter(
                name=unique_name, owner__username=request.user.username
            ):
                i = i + 1
                unique_name = "{0}-{1}".format(name, i)
            form.instance.name = unique_name
            organization = form.save()
            messages.success(request, "Organization created successfully.")
            return redirect(
                r("organizations:organization", kwargs={"org_name": organization.name})
            )
    else:
        form = CreateOrganizationForm()
    return render(request, "organizations/new.html", {"form": form})


# @member_required
@login_required
def organization(request, org_name):
    organization = Organization.objects.get(name=org_name)
    # get user's organizations
    user_organizations = request.user.profile.get_organizations()
    organization_datasets = organization.get_datasets()
    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save()
            messages.success(request, "Organization was saved successfully.")
            return redirect(r("organization", args=(organization.name)))
    else:
        form = OrganizationForm(instance=organization)
    return render(
        request,
        "organizations/single/data.html",
        {
            "organization": organization,
            "form": form,
            "user_organizations": user_organizations,
            "organization_datasets": organization_datasets,
        },
    )


# @member_required
@login_required
def view_members(request, org_name):
    username = request.user.username
    organization = Organization.objects.get(
        name=org_name, owner__username__iexact=username
    )
    members = organization.members.all()
    context = {"organization": organization, "members": members}
    return render(request, "organizations/members.html", context)


@main_owner_required
@login_required
@require_POST
def remove_owner_from_organization(request):
    try:
        owner_id = request.POST.get("user-id")
        organization_id = request.POST.get("organization-id")
        owner = User.objects.get(pk=owner_id)
        organization = Organization.objects.get(pk=organization_id)
        organization.members.remove(owner)
        organization.save()
        return HttpResponse()
    except Exception:
        return HttpResponseBadRequest()


# @member_required
@login_required
def leave(request):
    organization_id = request.POST.get("organization-id")
    organization = get_object_or_404(Organization, pk=organization_id)
    organization.members.remove(request.user)
    organization.save()
    messages.add_message(
        request,
        messages.SUCCESS,
        "You successfully left the organization {0}.".format(organization.title),
    )
    return redirect("/" + request.user.username + "/")
