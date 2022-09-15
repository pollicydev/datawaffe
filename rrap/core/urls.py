from django.urls import include, path
from .views import dashboard


urlpatterns = [
    path("", dashboard, name="dashboard"),
]