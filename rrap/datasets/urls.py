from django.urls import include, path

from rrap.datasets import views

app_name = "datasets"

urlpatterns = [
    path("", views.datasets, name="datasets"),
    path(
        "<str:org_name>/datasets/",
        views.datasets,
        name="datasets",
    ),
    path(
        "<str:org_name>/datasets/<str:dataset_name>",
        views.dataset,
        name="dataset",
    ),
    path("<str:org_name>/datasets/add/", views.new_dataset, name="add_data"),
]
