from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from store.admin import ProductModelAdmin
from store.models import Product
from tags.models import TaggedItem

# Register your models here.


class TagItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 1
    autocomplete_fields = ['tag']


admin.site.unregister(Product)

@admin.register(Product)
class CustomProductAdmin(ProductModelAdmin):
    inlines = [TagItemInline]