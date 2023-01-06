from django import forms
import django_filters
from rrap.core.models import KeyPopulation, Service, Issue
from rrap.organizations.models import OrganisationPage
from rrap.organizations.forms import OrganisationsFilterForm


class OrganisationsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm ps-5 text-white",
                "placeholder": "Search by name...",
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
        form = OrganisationsFilterForm