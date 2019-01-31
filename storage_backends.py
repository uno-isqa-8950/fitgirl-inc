
from storages.backends.s3boto3 import S3Boto3Storage

StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')

class S3MediaStorage(S3Boto3Storage):
    def __init__(self, **kwargs):
        kwargs['location'] = kwargs.get('location', 
            settings.MEDIA_ROOT.replace('/', ''))
        super(S3MediaStorage, self).__init__(**kwargs)
