from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    location = 'post_image'
    default_acl = None
    file_overwrite = False

class VideoStorage(S3Boto3Storage):
    location = 'post_video'
    default_acl = None
    file_overwrite  = False

class ProfileImageStorage(S3Boto3Storage):
    location = 'profile_image'
    default_acl = None
    file_overwrite  = False
