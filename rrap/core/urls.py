from django.urls import include, path

from rrap.core import views
from rrap.datasets import views as data_views

app_name = "core"


urlpatterns = [
    # public routes
    path("", views.home, name="home"),
    path("datasets/", views.datasets, name="datasets"),
    path("locations/", views.locations, name="locations"),
    path("organizations/", views.organizations, name="organizations"),
    # single public routes
    path("locations/<int:location_pk>/", views.location, name="single_location"),
    path("datasets/<uuid:dataset_uuid>", views.dataset, name="single_dataset"),
    path(
        "datasets/<uuid:dataset_uuid>/edit/",
        data_views.edit_dataset,
        name="edit_data",
    ),
    path("organizations/<str:org_name>/", views.organization, name="single_org"),
    path(
        "organizations/<str:org_name>/activity/",
        views.organization_activity,
        name="org_activity",
    ),
    path(
        "organizations/<str:org_name>/members/",
        views.organization_members,
        name="org_members",
    ),
    path(
        "organizations/<str:org_name>/followers/",
        views.organization_followers,
        name="org_followers",
    ),
]
