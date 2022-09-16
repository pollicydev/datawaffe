from django.http import Http404, HttpResponseBadRequest, HttpResponseForbidden

from rrap.organizations.models import Organization


def main_owner_required(f):
    def wrap(request, *args, **kwargs):
        if "org_name" in kwargs and "username" in kwargs:
            try:
                organization = Organization.objects.get(
                    name=kwargs["org_name"],
                    owner__username__iexact=kwargs["username"],
                )
                if organization.owner.id == request.user.id:
                    return f(request, *args, **kwargs)
                else:
                    raise Http404
            except Organization.DoesNotExist:
                raise Http404
        else:
            try:
                organization_id = request.POST["organization-id"]
            except Exception:
                try:
                    organization_id = request.GET["organization-id"]
                except Exception:
                    return HttpResponseBadRequest()

            organization = Organization.objects.get(pk=organization_id)
            if organization.owner.id == request.user.id:
                return f(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def member_required(f):
    def wrap(request, *args, **kwargs):
        if "org_name" in kwargs and "username" in kwargs:
            try:
                organization = Organization.objects.get(
                    name=kwargs["org_name"],
                    owner__username__iexact=kwargs["username"],
                )
                if organization.is_owner_or_member(request.user):
                    return f(request, *args, **kwargs)
                else:
                    raise Http404
            except Organization.DoesNotExist:
                raise Http404
        else:
            try:
                organization_id = request.POST["organization-id"]
            except Exception:
                try:
                    organization_id = request.GET["organization-id"]
                except Exception:
                    return HttpResponseBadRequest()
            organization = Organization.objects.get(pk=organization_id)
            if organization.is_owner_or_member(request.user):
                return f(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
