
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from storages.backends.s3boto3 import S3Boto3Storage


class PatchedS3StaticStorage(S3Boto3Storage):
    def _save(self, name, content):
        if hasattr(content, 'seek') and hasattr(content, 'seekable') and content.seekable():
            content.seek(0)
        return super()._save(name, content)


class CachedS3Storage(ManifestFilesMixin, PatchedS3StaticStorage):
    pass


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
