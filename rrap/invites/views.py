from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .constants import InviteStatus
from .forms import SendInviteForm
from .models import Invite
from rrap.organizations.mixins import MainOwnerRequiredMixin, OrganizationMixin
from ..utils.mask import mask_email


class ManageAccessView(
    LoginRequiredMixin,
    MainOwnerRequiredMixin,
    OrganizationMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = Invite
    form_class = SendInviteForm
    template_name = "invites/manage_access.html"

    def get_success_url(self):
        return reverse(
            "invites:manage_access",
            args=(self.organization.name),
        )

    def get_success_message(self, cleaned_data):
        return _("An invitation was sent to %s.") % self.object.get_invitee_email()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request, organization=self.organization)
        return kwargs

    def get_context_data(self, **kwargs):
        invites = self.organization.invites.select_related(
            "invited_by__profile", "invitee__profile"
        ).order_by("-date_sent")
        kwargs.update(invites=invites)
        return super().get_context_data(**kwargs)


class InviteDeleteView(
    LoginRequiredMixin, MainOwnerRequiredMixin, OrganizationMixin, DeleteView
):
    model = Invite
    pk_url_kwarg = "invite_id"
    context_object_name = "invite"

    def get_queryset(self):
        return self.organization.invites.filter(status=InviteStatus.PENDING)

    def get_success_url(self):
        return reverse(
            "invites:manage_access",
            args=(self.organization.name),
        )

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, _("The invitation was removed with success."))
        return response


class InviteDetailView(DetailView):
    model = Invite
    slug_field = "code"
    slug_url_kwarg = "code"
    context_object_name = "invite"

    def get_queryset(self):
        return Invite.objects.filter(status=InviteStatus.PENDING)

    def get_context_data(self, *args, **kwargs):
        args.update(self.organization.name)
        kwargs.update(invitee_masked_email=mask_email(self.object.get_invitee_email()))
        return super().get_context_data(**kwargs)


class UserInviteListView(LoginRequiredMixin, ListView):
    model = Invite
    context_object_name = "invites"
    template_name = "invites/user_invite_list.html"

    def get_queryset(self):
        return Invite.objects.select_related("invited_by__profile").filter(
            status=InviteStatus.PENDING, invitee=self.request.user
        )


class AcceptUserInviteView(LoginRequiredMixin, View):
    def post(self, request, invite_id):
        queryset = Invite.objects.filter(
            status=InviteStatus.PENDING, invitee=self.request.user
        )
        invite = get_object_or_404(queryset, pk=invite_id)
        invite.accept()
        messages.success(
            request,
            _("You have joined the organization %s.") % invite.organization.title,
        )
        return redirect(invite.organization)


class RejectUserInviteView(LoginRequiredMixin, View):
    def post(self, request, invite_id):
        queryset = Invite.objects.filter(
            status=InviteStatus.PENDING, invitee=self.request.user
        )
        invite = get_object_or_404(queryset, pk=invite_id)
        invite.reject()
        messages.success(
            request,
            _("You have rejected the invitation to join the organization %s.")
            % invite.organization.title,
        )
        return redirect("user_invites")
