from django import forms
from rrap.core.models import KeyPopulation, Service, Issue
from rrap.organizations.models import OrganisationPage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit, HTML, Div
from django_select2 import forms as s2forms


class MapFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["title"].label = ""
        self.fields["title"].wrapper_class = "extra-class"
        self.fields["communities"].label = ""
        self.fields["services"].label = ""
        self.fields["issues"].label = ""

    class Meta:
        model = OrganisationPage
        fields = ["title", "communities", "services", "issues"]
