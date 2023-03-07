from django import forms
import django_filters
from django.db.models.functions import ExtractYear
from rrap.organizations.models import OrganisationPage
from rrap.core.models import (
    KeyPopulation,
    Service,
    PublicationType,
    PublicationPage,
)
from rrap.core.forms import MapFilterForm, PubFilterForm


class MapFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm ps-5 text-white",
                "placeholder": "Filter by name...",
            }
        ),
    )
    org_type = django_filters.MultipleChoiceFilter(
        choices=OrganisationPage.ORG_TYPES,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )
    communities = django_filters.ModelMultipleChoiceFilter(
        queryset=KeyPopulation.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )
    services = django_filters.ModelMultipleChoiceFilter(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )
    toll_free = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(),
        method="unchecked_means_any_value",
    )

    def unchecked_means_any_value(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(toll_free__isnull=False)

    class Meta:
        model = OrganisationPage
        fields = "__all__"
        form = MapFilterForm


class PublicationsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm ps-5 text-white",
                "placeholder": "Filter by name...",
            }
        ),
    )
    pub_types = django_filters.ModelMultipleChoiceFilter(
        queryset=PublicationType.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )
    organisations = django_filters.ModelMultipleChoiceFilter(
        queryset=OrganisationPage.objects.all().order_by("title"),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )
    date_published = django_filters.MultipleChoiceFilter(
        choices=PublicationPage.objects.annotate(year=ExtractYear("date_published"))
        .values_list("year", "year")
        .distinct()
        .order_by(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-control form-control-sm"}
        ),
    )

    class Meta:
        model = PublicationPage
        fields = [
            "title",
            "pub_types",
            "date_published",
            "organisations",
        ]
        form = PubFilterForm
