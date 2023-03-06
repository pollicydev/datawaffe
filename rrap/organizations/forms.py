from django import forms
from .models import OrganisationPage, generate_logo
from crispy_forms.helper import FormHelper


class OrganisationsFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["title"].label = ""
        self.fields["communities"].label = ""
        self.fields["services"].label = ""
        self.fields["org_type"].label = ""
        self.fields["toll_free"].label = "With toll free"

    class Meta:
        model = OrganisationPage
        fields = ["title", "communities", "services", "org_type", "toll_free"]
