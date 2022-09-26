import base64
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.urls import reverse as r
from django.utils.translation import gettext
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from .decorators import member_required, main_owner_required
from .forms import (
    CreateOrganizationForm,
    OrganizationForm,
    EditOrganizationForm,
    OrganizationSettingsForm,
    DeleteLogoForm,
)
from .models import Organization, change_logo
from rrap.invites.constants import InviteStatus
from django.core.paginator import Paginator
from rrap.organizations.mixins import MainOwnerRequiredMixin, OrganizationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.files.base import ContentFile

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


@login_required
def update_logo(request, org_name):
    organization = Organization.objects.get(name=org_name)
    # Received base64 string starts with 'data:image/jpeg;base64,........'
    # We need to use 'jpeg' as an extension and everything after base64,
    # as the image itself:
    fmt, imgstr = request.POST["logo"].split(";base64")
    ext = fmt.split("/")[-1]
    if ext == "svg+xml":
        ext = "svg"
    img = ContentFile(base64.b64decode(imgstr), name=f"{organization.id}.{ext}")
    change_logo(organization, img)

    return redirect(r("organizations:edit", args=(organization.name)))


@login_required
def delete_logo(request, org_name):
    organization = Organization.objects.get(name=org_name)
    form = DeleteLogoForm(request.POST, instance=organization)
    form.save()

    return redirect(r("organizations:edit", args=(organization.name)))


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
            return redirect(r("organizations:organization", args=(organization.name)))
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


# @main_owner_required
@login_required
def edit_organization(request, org_name):
    organization = Organization.objects.get(name=org_name)
    if request.method == "POST":
        form = EditOrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save()
            messages.success(request, "Organization was saved successfully.")
            return redirect(r("organizations:edit", args=(organization.name,)))
    else:
        form = EditOrganizationForm(instance=organization)
    return render(
        request,
        "organizations/edit.html",
        {
            "organization": organization,
            "form": form,
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


# ORGANIZATION SETTINGS

# @main_owner_required
@login_required
def settings(request, org_name):
    username = request.user.username
    organization = Organization.objects.get(
        name=org_name, owner__username__iexact=username
    )
    if request.method == "POST":
        form = OrganizationSettingsForm(request.POST, instance=organization)
        if form.is_valid():
            name = slugify(form.instance.name)
            unique_name = name
            if unique_name != org_name:
                i = 0
                while Organization.objects.filter(
                    name=unique_name, owner__username=organization.owner.username
                ):
                    i = i + 1
                    unique_name = "{0}-{1}".format(name, i)
            form.instance.name = unique_name
            organization = form.save()
            messages.success(request, "Organization updated successfully.")
            return redirect(r("organizations:settings", args=(unique_name,)))
    else:
        form = OrganizationSettingsForm(instance=organization)
    return render(
        request,
        "organizations/settings.html",
        {"organization": organization, "form": form},
    )


# @main_owner_required
@login_required
def transfer(request):
    try:
        organization_id = request.POST["organization-id"]
        transfer_user_username = request.POST["transfer-user"]
        organization = Organization.objects.get(pk=organization_id)
        try:
            transfer_user = User.objects.get(username=transfer_user_username)
        except Exception:
            messages.warning(request, "User not found.")
            return redirect(
                "organizations:settings", organization.owner.username, organization.name
            )

        current_user = request.user
        if current_user != transfer_user:
            if transfer_user in organization.members.all():
                organization.members.remove(transfer_user)
            organization.owner = transfer_user
            organization.members.add(current_user)
            organization.save()
            return redirect(
                "organization", organization.owner.username, organization.name
            )
        else:
            messages.warning(
                request, "Hey! You can't transfer the organization to yourself."
            )
            return redirect(
                "organizations:settings", organization.owner.username, organization.name
            )

    except Exception:
        return HttpResponseBadRequest("Something went wrong.")


class DeleteOrganizationView(
    LoginRequiredMixin, MainOwnerRequiredMixin, OrganizationMixin, View
):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        self.organization.delete()
        messages.success(request, gettext("The organization was deleted with success."))
        return redirect(request.user)
