import logging
from datetime import datetime
from pathlib import Path
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse as r
from django.utils.text import slugify
from django.utils.html import escape
from .models import Dataset
from .forms import DatasetForm, EditDatasetForm
from django.core.paginator import Paginator
from django.views import View
from rrap.organizations.models import Organization
from rrap.organizations.decorators import member_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.files.storage import FileSystemStorage

logger = logging.getLogger(__name__)


def upload(request):

    if request.FILES["file"]:
        file = request.FILES["file"]
        fs = FileSystemStorage()
        uploaded_file = fs.save(file.name, file)
        uploaded_file_url = fs.url(uploaded_file)

        data = {
            "is_valid": True,
            "file_url": uploaded_file_url,
        }
    else:
        data = {"is_valid": False}

    return JsonResponse(data)


@login_required
def ajax_create_dataset(request):
    try:
        organization_id = request.GET.get("organization-id")
        organization = get_object_or_404(Organization, pk=organization_id)
        title = request.GET.get("file-name")
        title = Path(title).stem  # remove ext
        file_url = request.GET.get("file-url")
        file_mime = request.GET.get("file-mime")

        dataset = Dataset.objects.create(
            created_by=request.user,
            organization=organization,
            title=title,
            file_url=file_url,
            file_mime=file_mime,
        )

        uuid = dataset.get_uuid()

        return HttpResponse(uuid)

    except Exception:
        logger.exception("An error occurred while trying to get organization.")
        return HttpResponseBadRequest()


@login_required
def ajax_delete_file(request):
    try:
        organization_id = request.GET.get("organization-id")
        organization = get_object_or_404(Organization, pk=organization_id)
        title = request.GET.get("file-name")
        title = Path(title).stem  # remove ext
        file_url = (request.GET.get("file-url"),)
        file_mime = (request.GET.get("file-mime"),)

        dataset = Dataset.objects.create(
            created_by=request.user,
            organization=organization,
            title=title,
            file_url=file_url,
            file_mime=file_mime,
        )

        uuid = dataset.get_uuid()

        return HttpResponse(uuid)

    except Exception:
        logger.exception("An error occurred while trying to get organization.")
        return HttpResponseBadRequest()


@login_required
@member_required
def new(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)

    return render(
        request,
        "datasets/new.html",
        {"organization": organization},
    )


@login_required
@member_required
def new_dataset(request, org_name):
    organization = get_object_or_404(Organization, name=org_name)

    if request.method == "POST":
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
            form.instance.organization = organization
            dataset = form.save(commit=False)
            # Save file information to db
            dataset.file_mime = request.FILES["file"].content_type
            dataset.save()
            messages.success(request, "Dataset saved successfully.")
            return redirect(
                r(
                    "core:single_dataset",
                    args=(dataset.uuid,),
                )
            )
    else:
        form = DatasetForm()
    return render(
        request,
        "datasets/edit.html",
        {"form": form, "organization": organization},
    )


@login_required
def dataset(request, org_name, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name, organization__name=org_name)

    if request.method == "POST":
        form = DatasetForm(request.POST, request.FILES, instance=dataset)
        print(form.errors)
        if form.is_valid():
            name = slugify(form.instance.title)
            if not name:
                name = "dataset"
            unique_name = name
            i = 0
            while Dataset.objects.filter(name=unique_name):
                i = i + 1
                unique_name = "{0}-{1}".format(name, i)
            form.instance.name = unique_name
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
            # dataset = form.save(commit=False)
            # dataset.start_date = datetime.strptime(
            #     request.POST["start_date"], "%d-%m-%Y"
            # )
            # dataset.end_date = datetime.strptime(request.POST["end_date"], "%d-%m-%Y")
            # dataset.save()
            dataset = form.save()
            messages.success(request, "Dataset was saved successfully.")
            return redirect(r("core:single_dataset", args=(dataset.uuid,)))
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
