from django import forms
import django_filters
from rrap.core.models import KeyPopulation, Service
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
        form = OrganisationsFilterForm
