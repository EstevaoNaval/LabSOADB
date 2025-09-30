from django.apps import AppConfig
from rest_framework.fields import FileField as DRFFileField
from urllib.parse import urlparse
from django.conf import settings

class ChemicalsConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "chemicals"
    
    def _to_rel(self, value):
        if not value:
            return None
        
        try:
            url = value.url
        except Exception:
            return None
        
        # if it's already relative, leave it
        parsed = urlparse(url)
        if not parsed.netloc:
            return url
        
        # OPTIONAL: only strip known host(s); change this logic if needed
        # allowed_hosts might include 'django-api:8000' or production host
        host_ok = any(parsed.netloc.endswith(h) for h in getattr(settings, "HOSTS_TO_STRIP", []))
        if host_ok:
            return parsed.path
        
        # otherwise return full url (keeps presigned S3 urls intact)
        return url
    
    def ready(self):
        

        DRFFileField.to_representation = self._to_rel
