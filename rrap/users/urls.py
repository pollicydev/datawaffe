from django.urls import path
from django.views.generic import RedirectView
from rrap.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    update_profile,
    update_avatar,
    user_delete_account,
    delete_avatar,
    onboard_user
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("edit_profile/", view=update_profile, name="update_profile"),
    path("delete/", view=user_delete_account, name="delete"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("avatar/update/", view=update_avatar, name="update_avatar"),
    path("avatar/delete/", view=delete_avatar, name="delete_avatar"),
    path(
        "onboarding/",
        RedirectView.as_view(pattern_name="onboard_user"),
        name="onboarding",
    ),
    path("onboarding/profile", view=onboard_user, name="onboarding"),
]
