from django.urls import include, path

from rrap.organizations import views
from rrap.invites import views as invite_views

app_name = "organizations"

urlpatterns = [
    path("", views.organizations, name="organizations"),
    path(
        "<str:org_name>/",
        views.organization,
        name="organization",
    ),
    path(
        "<str:org_name>/edit",
        views.edit_organization,
        name="edit",
    ),
    path(
        "<str:org_name>/members/",
        views.view_members,
        name="members",
    ),
    path("request/new/", views.new, name="new"),
    path(
        "remove_owner/",
        views.remove_owner_from_organization,
        name="remove_owner_from_organization",
    ),
    path("leave/", views.leave, name="leave"),
    path(
        "<str:org_name>/settings/",
        views.settings,
        name="settings",
    ),
    path(
        "transfer/",
        views.transfer,
        name="transfer_organization",
    ),
    path(
        "<str:org_name>/settings/delete/",
        views.DeleteOrganizationView.as_view(),
        name="delete_organization",
    ),
    path("<str:org_name>/logo/update/", views.update_logo, name="update_logo"),
    path("<str:org_name>/logo/delete/", views.delete_logo, name="delete_logo"),
    # Invitation routes
    path(
        "<str:org_name>/members/invites/",
        invite_views.ManageAccessView.as_view(),
        name="manage_access",
    ),
    # path("<str:org_name>/members/invites/list/", invite_views.UserInviteListView.as_view(), name="user_invites"),
    path(
        "<str:org_name>/members/invites/<int:invite_id>/accept/",
        invite_views.AcceptUserInviteView.as_view(),
        name="accept_user_invite",
    ),
    path(
        "<str:org_name>/members/invites/<int:invite_id>/reject/",
        invite_views.RejectUserInviteView.as_view(),
        name="reject_user_invite",
    ),
    path(
        "<str:org_name>/members/invites/<uuid:code>/",
        invite_views.InviteDetailView.as_view(),
        name="invite",
    ),
]
