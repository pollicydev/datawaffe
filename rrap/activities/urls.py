from django.urls import path

from rrap.activities import views

app_name = "activities"

urlpatterns = [
    path("<str:org_slug>/follow/", views.follow, name="follow"),
    path("<str:org_slug>/unfollow/", views.unfollow, name="unfollow"),
    path(
        "<str:org_slug>/update_followers_count/",
        views.update_followers_count,
        name="update_followers_count",
    ),
]
