from storages.backends.s3boto3 import S3Boto3Storage
from filebrowser_safe.storage import S3BotoStorageMixin

# Media files are not public. Only authorized users should have access.
class PublicMediaStorage(S3BotoStorageMixin, S3Boto3Storage):
    location = 'media'
    default_acl = None
    file_overwrite = True
