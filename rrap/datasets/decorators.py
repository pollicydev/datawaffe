from django.core.exceptions import PermissionDenied
from rrap.datasets.models import Dataset


def privacy_check(f):
    def wrap(request, *args, **kwargs):
        if "dataset_uuid" in kwargs:
            try:
                dataset = Dataset.objects.get(uuid=kwargs["dataset_uuid"])
                if dataset.is_public() or dataset.is_request_only():
                    return f(request, *args, **kwargs)

                if dataset.is_private():
                    raise PermissionDenied

                else:
                    raise PermissionDenied
            except Dataset.DoesNotExist:
                raise PermissionDenied

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
