from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.contrib import messages
from rrap.users.decorators import onboarding_required

@login_required()
@onboarding_required()
def dashboard(request):
    profile = request.user.profile

    # first check if user is not staff and has whether has finished registration via onboarding
    if not request.user.is_staff and not request.user.profile.has_finished_registration:
        return redirect("users:onboarding")

    if request.user.is_staff:
        return redirect("/admin")

    # Check if user has verified email
    verified = ""
    if EmailAddress.objects.filter(user=request.user, verified=True).exists():
        pass
    else:
        verified = False
        messages.warning(
            request,
            "We sent a verification link to your email account. Please click the link to fully activate your account.",
        )
    context = {
        "profile": profile,
        "verified": verified,
    }

    return render(request, "core/dashboard.html", context)
