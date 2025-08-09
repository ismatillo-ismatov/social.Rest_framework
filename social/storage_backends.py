from storages.backends.gcloud import GoogleCloudStorage

class PublicMediaStorage(GoogleCloudStorage):
    location = 'post_image'
    # default_acl = 'publicRead'
    file_overwrite = False

class VideoStorage(GoogleCloudStorage):
    location = 'post_video'
    # default_acl = 'publicRead'
    file_overwrite  = False

class ProfileImageStorage(GoogleCloudStorage):
    location = 'profile_image'
    # default_acl = 'publicRead'
    file_overwrite  = False
