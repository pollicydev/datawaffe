from django import forms
from rrap.organizations.models import OrganisationPage
from rrap.core.models import PublicationPage
from crispy_forms.helper import FormHelper


class MapFilterForm(forms.Form):
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


class PubFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["title"].label = ""
        self.fields["pub_types"].label = ""
        self.fields["organisations"].label = ""
        self.fields["date_published"].label = ""

    class Meta:
        model = PublicationPage
        fields = ["title", "pub_types", "organisations", "date_published"]
