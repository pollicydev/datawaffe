from django.urls import include, path

from rrap.core import views

app_name = "core"


urlpatterns = [
    path("", views.home, name="home"),
    path("datasets/", views.datasets, name="datasets"),
    path("locations/", views.locations, name="locations"),
    path("organizations/", views.organizations, name="organizations"),
]
