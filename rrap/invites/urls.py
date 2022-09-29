from django.urls import path

from rrap.invites import views

app_name = "invitations"

urlpatterns = [
    path("", views.ManageAccessView.as_view(), name="manage_access"),
    path(
        "<uuid:code>/",
        views.InviteDetailView.as_view(),
        name="invite",
    ),
    path(
        "<int:invite_id>/accept/",
        views.AcceptUserInviteView.as_view(),
        name="accept_user_invite",
    ),
    path(
        "<int:invite_id>/reject/",
        views.RejectUserInviteView.as_view(),
        name="reject_user_invite",
    ),
]
