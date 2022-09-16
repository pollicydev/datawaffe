from django.urls import include, path

from rrap.organizations import views

app_name = "organisations"

urlpatterns = [
    path("", views.remove_owner_from_organization, name="organisations"),
    path(
        "organizations/<str:org_name>/",
        views.organization,
        name="organisation",
    ),
    path(
        "organizations/<str:org_name>/members/",
        views.view_members,
        name="members",
    ),
    path("organizations/", views.organizations, name="organizations"),
    path("new/", views.new, name="new"),
    path(
        "remove_owner/",
        views.remove_owner_from_organization,
        name="remove_owner_from_organization",
    ),
    path("leave/", views.leave, name="leave"),
    path(
        "organizations/<str:org_name>/members/invites/",
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
