from urllib.parse import urlencode
from django.contrib import admin, messages
from django.urls import reverse
from django.db.models import Count
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline

from . import models

# Register your models here.

@admin.register(models.Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    # Dynamically get all field names from the model
    ordering = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'membership', 'customer_address', 'orders_count']
    empty_value_display = "-empty-"
    list_editable=['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


    list_select_related = True
    list_per_page = 10
    

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            +urlencode({
                "customer__id": str(customer.id)
                })
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)
        # return customer.orders_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('customer_orders')
        )
    
    


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory status'
    parameter_name = 'inventory'
    LOW_STOCK = "<10"
    OUT_OF_STOCK = "0"

    def lookups(self, request, model_admin):
        return [
            (self.LOW_STOCK, 'Low'),
            (self.OUT_OF_STOCK, 'Out of Stock'),
        ]
    
    def queryset(self, request, queryset):
       if self.value() == self.LOW_STOCK:
           return queryset.filter(inventory__lt=10)
       elif self.value() == self.OUT_OF_STOCK:
           return queryset.filter(inventory=0)
       return queryset




@admin.register(models.Product)
class ProductModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['name']
    } # to prepopulate slug field based on name field
    autocomplete_fields = ['collection'] # to enable autocomplete for foreign key fields, because collection can have many entries 
    # like many 1000s of collections, so its better to have autocomplete (search) rather than getting all values dropdown
    # exclude = ['promotions'] 
    # form editing -> adding/editing products won't show if we add in exclude,
    # if we add in fields -> only show those fields in the form

    actions = ['clear_inventory']
    list_display = ['name', 'unit_price', 'inventory_status', 'collection_title', 'last_updated']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['name']
    list_filter = ['collection', 'last_updated', InventoryFilter]


    @admin.display(ordering='collection__title', description='Collection')
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory == 0:
            return "Out of Stock"
        elif product.inventory < 10:
            return "Low"
        return "Ok"
    
    @admin.action(description="Clear Inventory of selected products")
    def clear_inventory(self, request, queryset):
        count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{count} products inventory were successfully cleared.",
            messages.SUCCESS
        )


class OrderItemsInlineEdit(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 3
    autocomplete_fields = ['product']



@admin.register(models.Order)
class OrderModelAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInlineEdit]

    autocomplete_fields = ['customer']
    
    list_display = ['id', 'placed_at', 'customer_full_name', 'payment_status']
    list_select_related = ['customer']
    list_editable = ['payment_status']
    list_per_page = 10

    @admin.display(ordering='customer__first_name')
    def customer_full_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'count']
    list_per_page = 10
    search_fields = ['title']

    @admin.display(ordering='products_count', description='Products Count')
    def count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({
                'collection__id': str(collection.id)
            })
        )
        return format_html("<a href={}>{}</a>", url, collection.products_count)
        # return collection.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )