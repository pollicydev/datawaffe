import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse as r
from django.utils.text import slugify
from django.utils.html import escape
from .models import Dataset
from .forms import NewDatasetForm, DatasetForm, EditDatasetForm
from django.core.paginator import Paginator
from django.views import View
from rrap.organizations.models import Organization
from rrap.organizations.decorators import member_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
@member_required
def new_dataset(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)

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
            # Save file information to db
            dataset.file_mime = request.FILES["file"].content_type
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
        form = DatasetForm(request.POST, request.FILES, instance=dataset)
        print(form.errors)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.status = 1
            dataset.save()
            form.save_m2m()  # save the tags too
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


@login_required
def edit_dataset(request, dataset_uuid):
    dataset = Dataset.objects.get(uuid=dataset_uuid)
    if request.method == "POST":
        form = EditDatasetForm(request.POST, instance=dataset)
        if form.is_valid():
            dataset = form.save()
            messages.success(request, "Dataset was saved successfully.")
            return redirect(r("data:dataset", args=(dataset.uuid,)))
    else:
        form = EditDatasetForm(instance=dataset)
    return render(
        request,
        "datasets/edit.html",
        {
            "dataset": dataset,
            "form": form,
        },
    )
