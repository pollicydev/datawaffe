
import base64
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib.auth.decorators import login_required
from .forms import DeleteUserForm
from .utils import DeleteAvatarForm, OnboardingForm, ProfileForm
from .models import change_avatar
from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.files.base import ContentFile

User = get_user_model()

@login_required()
def update_profile(request):

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your profile was successfully updated!"))
            return redirect(reverse("users:update_profile"))
        else:
            messages.error(request, _("Please correct the error(s) below."))
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(
        request, "users/edit_profile.html", {
            "form": form,
            "delete_user_form": DeleteUserForm(user=User)
            }
    )


@login_required
def update_avatar(request):
    user = request.user.profile
    # Received base64 string starts with 'data:image/jpeg;base64,........'
    # We need to use 'jpeg' as an extension and everything after base64,
    # as the image itself:
    fmt, imgstr = request.POST["avatar"].split(";base64")
    ext = fmt.split("/")[-1]
    if ext == "svg+xml":
        ext = "svg"
    img = ContentFile(base64.b64decode(imgstr), name=f"{user.id}.{ext}")
    change_avatar(user, img)

    return redirect(reverse("users:update_profile"))


@login_required
def delete_avatar(request):
    user = request.user.profile
    form = DeleteAvatarForm(request.POST, instance=user)
    form.save()

    return redirect(reverse("users:update_profile"))

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

#delete user account
@login_required
def user_delete_account(request):
    form = DeleteUserForm(request.user, request.POST)
    if form.is_valid():
        form.save()
        return redirect("/")

    messages.error(request, _("Couldn't delete your account. It is possible your password was incorrect."))
    return redirect(reverse("users:update_profile"))


# onboarding
def onboard_user(request):
    profile = request.user.profile
    if request.method == "POST":
        form = OnboardingForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            profile.has_finished_registration = True
            form.save()
            return redirect("dashboard")
    else:
        form = OnboardingForm(instance=profile)
    return render(request, "account/onboarding.html", {"form": form})

