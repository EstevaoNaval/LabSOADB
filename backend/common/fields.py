from urllib.parse import urlparse

from rest_framework import serializers

class RelativePathFileField(serializers.FileField):
    """
    A custom serializer field that returns the relative path of a file.
    """
    def to_representation(self, value):
        # If the file doesn't exist or has no URL, return None
        if not value or not hasattr(value, 'url'):
            return None
        
        # The 'value.url' attribute already holds the relative path,
        # like '/media/path/to/file.json'. We simply return it.
        parsed = urlparse(value.url)
        return parsed.path if parsed.netloc else value.url
    
class RelativePathImageField(RelativePathFileField, serializers.ImageField):
    """
    A custom serializer field that returns the relative path of a image.
    """