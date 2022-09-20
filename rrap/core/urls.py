from django.urls import include, path

from rrap.core import views

app_name = "core"


urlpatterns = [
    # public routes
    path("", views.home, name="home"),
    path("datasets/", views.datasets, name="datasets"),
    path("locations/", views.locations, name="locations"),
    path("organizations/", views.organizations, name="organizations"),
    # single public routes
    path("datasets/<uuid:dataset_uuid>", views.dataset, name="single_dataset"),
    path("organizations/<str:org_name>", views.organization, name="single_org"),
]
