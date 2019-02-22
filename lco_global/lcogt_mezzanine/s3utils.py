from storages.backends.s3boto import S3BotoStorage
from filebrowser_safe.storage import S3BotoStorageMixin

class S3Storage(S3BotoStorageMixin, S3BotoStorage):
   pass
