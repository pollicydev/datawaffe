from django import forms
from rrap.blog.models import BlogPage
from crispy_forms.helper import FormHelper


class BlogFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["title"].label = ""
        self.fields["blog_page_type"].label = ""
        self.fields["organisations"].label = ""
        self.fields["topics"].label = ""

    class Meta:
        model = BlogPage
        fields = ["title", "blog_page_type", "organisations", "topics"]
