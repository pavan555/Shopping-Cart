from django.shortcuts import render, HttpResponse
from django.db.models import Q, F
from store.models import Product, OrderItem, Order

# Create your views here.


def say_hello_to_my_project(request):
    query_set = Product.objects.filter(Q(name__icontains="coffee") | Q(unit_price__gte=20, inventory__gte=25))
    products = list(Product.objects.filter(unit_price__gt=F('inventory')))
    # count = Product.objects.filter(name__icontains="coffee").count()
    # print(count)

    # list(query_set)
    # return HttpResponse("Hola from Project app!")
    return get_last_5_orders(request)
    # return render(request, 'hello.html', {'name': 'Project App', "products": list(query_set)})


def get_orders(request):
    # orders = OrderItem.objects.order_by('product__name').values('id', 'product__name', 'units', 'price')

    ids = OrderItem.objects.values('product_id').distinct()
    products = Product.objects.filter(id__in=ids).order_by('name').values('id', 'name', 'unit_price')
    return render(request, 'orders.html', {'orders': products})


def get_products_data(request):
    # select_related for 1 relationships (ForeignKey, OneToOneField) 
    # prefetch_related for many relationships (ManyToManyField, Reverse ForeignKey)
    # order doesnt matter for select_related and prefetch_related
    products = Product.objects.select_related('collection').prefetch_related('promotions').all()[:10]
    return render(request, 'orders.html', {'orders': products})


def get_last_5_order_items(request):
    last_5_orders = OrderItem.objects.select_related('order', 'order__customer', 'product').order_by('-order__placed_at')[:5]
    return render(request, 'orders.html', {'orderitems': last_5_orders})

def get_last_5_orders(request):
    last_5_orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    return render(request, 'orders.html', {'orderitems': last_5_orders})

def say_goodbye_to_my_project(request):
    goodbye_message = "Goodbye from Project app! See you again!"
    return render(request, 'bye.html', {'goodbye_message': goodbye_message})