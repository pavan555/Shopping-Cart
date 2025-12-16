from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):

    def get_tag_items_for_obj_type(self, object_type, object_id):
        content_type = ContentType.objects.get_for_model(object_type)
        return self.filter(content_type=content_type, object_id=object_id)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # The type of object being tagged (e.g., 'product', 'collection', etc.)
    # object_id to fetch object based on id & type
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')