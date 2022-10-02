from django.urls import include, path

from rrap.datasets import views
from rrap.core import views as core_views

app_name = "data"

urlpatterns = [
    path("", core_views.datasets, name="datasets"),
    path("<str:org_name>/add/", views.new_dataset, name="add_data"),
    path("upload/", views.upload, name="upload"),
]
