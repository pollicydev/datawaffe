from allauth.account.forms import SignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div
from .utils import PasswordProtectedForm
from allauth.account.forms import (
    LoginForm,
    ResetPasswordForm,
    AddEmailForm,
    ChangePasswordForm,
)

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class DeleteUserForm(PasswordProtectedForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self):
        self.user.delete()


class UserSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lets make all fields big by default to catch the passwords too
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control form-control-lg ps-5"
            if field_name == "password2":
                field.widget.attrs["placeholder"] = "Confirm password"
            elif field_name == "email":
                field.widget.attrs["placeholder"] = "Enter email address"
            elif field_name == "password1":
                field.widget.attrs["placeholder"] = "Enter password"
        self.helper = FormHelper(self)
        self.helper.layout = Layout("email", "password1", "password2")
        # Edit labels for obvious reasons.
        self.fields["email"].label = ""
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control form-control-lg ps-5"

        self.helper = FormHelper(self)
        self.helper.layout = Layout("login", "password")
        # Edit labels for obvious reasons.
        self.fields["login"].label = ""
        self.fields["password"].label = ""


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control  form-control-lg ps-5"

        self.helper = FormHelper(self)
        self.helper.layout = Layout("email")
        # Edit labels for obvious reasons.
        self.fields["email"].label = ""


class CustomAddEmailForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super(CustomAddEmailForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
