from django.conf import settings

CRYPTAPI_URL = getattr(settings, 'CRYPTAPI_URL', "https://cryptapi.io/api/")
