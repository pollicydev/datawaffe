import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse as r
from django.utils.text import slugify
from django.utils.html import escape
from .models import Dataset
from .forms import NewDatasetForm, DatasetForm
from django.core.paginator import Paginator
from django.views import View
from rrap.organizations.models import Organization
from rrap.organizations.decorators import member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


@login_required
def datasets(request, org_name):
    username = request.user.username
    organization = get_object_or_404(
        Organization, name=org_name, owner__username__iexact=username
    )

    try:
        datasets = organization.get_projects()
    except Dataset.DoesNotExist:
        datasets = None

    return render(
        request,
        "datasets/index.html",
        {"datasets": datasets, "organization": organization},
    )


@login_required
def new_dataset(request, org_name):
    username = request.user.username
    organization = get_object_or_404(
        Organization, name=org_name, owner__username__iexact=username
    )

    if request.method == "POST":
        form = NewDatasetForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
            form.instance.organization = organization
            name = slugify(form.instance.title)
            if not name:
                name = "dataset"
            unique_name = name
            i = 0
            while Dataset.objects.filter(
                name=unique_name, organization=organization.id
            ):
                i = i + 1
                unique_name = "{0}-{1}".format(name, i)
            form.instance.name = unique_name
            dataset = form.save(commit=False)
            # get mime type on save
            dataset.mime = request.FILES["file"].content_type
            dataset.save()
            messages.success(request, "Dataset saved successfully.")
            return redirect(
                r(
                    "datasets:dataset",
                    args=(dataset.organization.name, dataset.name),
                )
            )
    else:
        form = NewDatasetForm()
    return render(
        request,
        "datasets/new.html",
        {"form": form, "organization": organization},
    )


@login_required
def dataset(request, org_name, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name, organization__name=org_name)

    if request.method == "POST":
        form = DatasetForm(request.POST, instance=dataset)
        if form.is_valid():
            dataset = form.save()
            messages.success(request, "Dataset details saved successfully.")
            return redirect(
                r("datasets:dataset", args=(dataset.organization.name, dataset.name))
            )

    else:
        form = DatasetForm(instance=dataset)

    return render(
        request,
        "datasets/dataset.html",
        {
            "dataset": dataset,
            "form": form,
        },
    )
