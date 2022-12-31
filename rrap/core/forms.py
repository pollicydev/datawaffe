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
        self.fields["issues"].label = ""

    class Meta:
        model = OrganisationPage
        fields = ["title", "communities", "services", "issues"]


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
