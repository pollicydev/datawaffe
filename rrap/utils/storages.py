from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
