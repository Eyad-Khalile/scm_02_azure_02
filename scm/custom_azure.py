from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'scgmedia' # Must be replaced by your <storage_account_name>
    account_key = 'AFw4N7lUuSufM0HIaC9ESlXdRCpb16NZUgbuTN8KT7fNf0WP9zh66s+CQaimc+iRjJxdusRLg+baHS2etL8BgQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'scgmedia' # Must be replaced by your storage_account_name
    account_key = 'AFw4N7lUuSufM0HIaC9ESlXdRCpb16NZUgbuTN8KT7fNf0WP9zh66s+CQaimc+iRjJxdusRLg+baHS2etL8BgQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None