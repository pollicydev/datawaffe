from django.urls import include, path

from rrap.organizations import views

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
        "<str:org_name>/members/invites/",
        include("rrap.invites.urls", namespace="invites"),
    ),
    # path(
    #     "organizations/<str:org_name>/info/",
    #     views.info,
    #     name="info",
    # ),
    # path(
    #     "organizations/<str:org_name>/settings/",
    #     views.settings,
    #     name="settings",
    # ),
    # path(
    #     "organizations/<str:org_name>/settings/delete/",
    #     views.DeleteOrganizationView.as_view(),
    #     name="delete_organization",
    # ),
]
