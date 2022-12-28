from django import forms
import django_filters
from rrap.organizations.models import OrganisationPage, OrganisationPublication
from rrap.core.models import KeyPopulation, Service, Issue, PublicationType
from rrap.core.forms import MapFilterForm, PubFilterForm
from django_select2 import forms as s2forms


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
    issues = django_filters.ModelMultipleChoiceFilter(
        queryset=Issue.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )

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
    page = django_filters.ModelMultipleChoiceFilter(
        queryset=OrganisationPage.objects.all().order_by("title"),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = OrganisationPublication
        fields = "__all__"
        form = PubFilterForm
