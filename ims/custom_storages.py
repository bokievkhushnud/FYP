from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs["default_acl"] = "public-read"
        super().__init__(*args, **kwargs)
