from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import get_storage_class


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
