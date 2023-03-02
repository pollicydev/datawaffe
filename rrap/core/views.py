import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.contrib import messages
from rrap.users.decorators import onboarding_required
from rrap.organizations.decorators import member_required, main_owner_required
from rrap.organizations.models import (
    OrganisationPage,
    OrganisationPublication,
)
from rrap.core.models import Location
from .models import Location, Topic
from hitcount.utils import get_hitcount_model
from hitcount.views import _update_hit_count
from django.views.decorators.http import require_http_methods
from .filters import MapFilter, PublicationsFilter
from django.views.decorators.http import require_GET
from django.http import HttpResponse, HttpRequest
from django_htmx.middleware import HtmxDetails

from django.views.generic import TemplateView


class Handler500(TemplateView):
    template_name = "500.html"

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request):
            r = v(request)
            r.render()
            return r

        return view

    # must also override this method to ensure the 500 status code is set
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=500)


# Typing pattern recommended by django-stubs:
# https://github.com/typeddjango/django-stubs#how-can-i-create-a-httprequest-thats-guaranteed-to-have-an-authenticated-user
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# @login_required
# @onboarding_required
def home(request):

    if request.user.is_authenticated:

        # first check if user is not staff and has whether has finished registration via onboarding
        if (
            not request.user.is_staff
            and not request.user.profile.has_finished_registration
        ):
            return redirect("users:onboarding")

        if request.user.is_staff:
            return redirect("/cms")

        # Check if user has verified email
        verified = False
        if EmailAddress.objects.filter(user=request.user, verified=True).exists():
            pass
        else:
            verified = False
            messages.warning(
                request,
                "We sent a verification link to your email account. Please click the link to fully activate your account.",
            )

    context = {
        "verified": verified,
    }

    return render(request, "core/home.html", context)


@require_GET
def map(request: HtmxHttpRequest) -> HttpResponse:
    organisations = OrganisationPage.objects.live().public().order_by("title")
    org_filter = MapFilter(request.GET, queryset=organisations)
    filtered_districts = org_filter.qs.values_list("locations", flat=True)
    list_districts = Location.objects.filter(id__in=filtered_districts).values_list(
        "name", flat=True
    )
    districts = json.dumps(list(list_districts))

    # wait for filter get request for map organisations
    if request.htmx:
        base_template = "partials/organisations.html"
    else:
        base_template = "core/map.html"

    context = {
        "organisations": org_filter.qs,
        "map_filter_form": org_filter.form,
        "districts": districts,
    }
    return render(request, base_template, context)


@require_GET
def publications_index(request: HtmxHttpRequest) -> HttpResponse:
    publications = OrganisationPublication.objects.all().order_by("title")
    pub_filter = PublicationsFilter(request.GET, queryset=publications)

    # wait for filter get request for map organisations
    if request.htmx:
        base_template = "partials/publications.html"
    else:
        base_template = "core/publications.html"

    context = {
        "publications": pub_filter.qs,
        "pub_filter_form": pub_filter.form,
    }
    return render(request, base_template, context)


def single_publication(request, slug):
    organisation = OrganisationPage.objects.get(slug=slug)

    context = {"organisation": organisation}

    return render(request, "organizations/single.html", context)


@require_http_methods(["POST", "GET"])
def search(request):

    context, query_dict = {}, {}
    # use template partial for htmx requests
    template_name = "core/home.html"
    if request.htmx:
        template_name = "partials/organisations.html"
    else:
        context.update(
            OrganisationPage.objects.live().public().order_by("-first_published_at")
        )

    # fetch and format search query parameters
    query_dict = request.GET if request.method == "GET" else request.POST
    opt_params = get_opt_params(query_dict)
    query = query_dict.get("query", None)

    # fetch results from the index and add them to the context
    results = search_index.search(query=query, opt_params=opt_params)
    next_offset = opt_params.get("offset", 0) + 20  # similar to pagination,
    context.update(
        {
            "organisations": results["hits"],
            # "total": results["nbHits"],
            "processing_time": results["processingTimeMs"],
            "next_offset": next_offset,
        }
    )
    return render(request, template_name, context)
