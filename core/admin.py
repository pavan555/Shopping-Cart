from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User
from store.admin import ProductModelAdmin
from store.models import Product
from tags.models import TaggedItem

# Register your models here.

# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )

class TagItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 1
    autocomplete_fields = ['tag']


admin.site.unregister(Product)

@admin.register(Product)
class CustomProductAdmin(ProductModelAdmin):
    
    def get_inlines(self, request, obj):
        return super().get_inlines(request, obj) + [TagItemInline]