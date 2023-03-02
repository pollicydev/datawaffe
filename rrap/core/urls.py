from django.urls import include, path

from rrap.core import views

app_name = "core"


urlpatterns = [
    # public routes
    path("", views.home, name="home"),
    path("search", views.search, name="search"),
]
