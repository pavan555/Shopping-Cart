from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
# Create your models here.

class LikedItem(models.Model):
    liked_at = models.DateTimeField(auto_now_add=True)
    # type of object that user liked (e.g., 'product', 'collection', etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)