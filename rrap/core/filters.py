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


class EmptyChoiceField(forms.ChoiceField):
    def __init__(
        self,
        choices=(),
        empty_label=None,
        required=True,
        widget=None,
        label=None,
        initial=None,
        help_text=None,
        *args,
        **kwargs
    ):

        # prepend an empty label if it exists (and field is not required!)
        if not required and empty_label is not None:
            choices = tuple([("", empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(
            choices=choices,
            required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            *args,
            **kwargs
        )


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
    year = django_filters.MultipleChoiceFilter(
        choices=OrganisationPublication.objects.values_list("year", "year")
        .distinct()
        .order_by(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-control form-control-sm"}
        ),
    )

    class Meta:
        model = OrganisationPublication
        fields = "__all__"
        form = PubFilterForm
