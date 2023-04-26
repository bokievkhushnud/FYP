import os
from storages.backends.s3boto3 import S3Boto3Storage
AWS_STORAGE_BUCKET_NAME = os.environ.get('BUCKETEER_BUCKET_NAME')

class PublicMediaStorage(S3Boto3Storage):
    location = 'public'
    default_acl = None  # Remove the ACL setting
    file_overwrite = False
    custom_domain = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{location}'
