from django.db.models import Q
from .models import Dataset
from rrap.core.models import Location
from django.shortcuts import render, redirect, get_object_or_404


def is_valid_queryparam(param):
    return param != "" and param is not None


def dataset_filter(request):
    qs = Dataset.objects.filter(status=1)
    title_contains_query = request.GET.get("title_contains")
    mime_exact_query = request.GET.get("mime_exact")
    organization_query = request.GET.get("organization")
    location = request.GET.get("location")

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    elif is_valid_queryparam(mime_exact_query):
        qs = qs.filter(id=mime_exact_query)

    elif is_valid_queryparam(organization_query):
        qs = qs.filter(organization__name=organization_query)

    if is_valid_queryparam(location) and location != "Choose...":
        qs = qs.filter(locations__pk=location)

    return qs


def location_based_filter(request, location_pk):
    location = get_object_or_404(Location, pk=location_pk)
    qs = location.datasets.all()
    title_contains_query = request.GET.get("title_contains")
    mime_exact_query = request.GET.get("mime_exact")
    organization_query = request.GET.get("organization")
    location = request.GET.get("location")

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    elif is_valid_queryparam(mime_exact_query):
        qs = qs.filter(id=mime_exact_query)

    elif is_valid_queryparam(organization_query):
        qs = qs.filter(organization__name=organization_query)

    if is_valid_queryparam(location) and location != "Choose...":
        qs = qs.filter(locations__pk=location)

    return qs
