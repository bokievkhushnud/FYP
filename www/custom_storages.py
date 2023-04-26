from storages.backends.s3boto3 import S3Boto3Storage

class PublicS3Boto3Storage(S3Boto3Storage):
    querystring_auth = False