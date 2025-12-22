from django.shortcuts import render, HttpResponse
from django.db.models import Q, F, Func, Value
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage, mail_admins
from templated_email import send_templated_mail


from store.models import Product, OrderItem, Order, Customer
from tags.models import TaggedItem
from .tasks import notify_customers


def send_template_mail():
    try:
        recipient_list = ["admin@storefront.com", "pavan@storefront.com", "user@storefront.com"]
        send_templated_mail(
            template_name= "hello",
            template_prefix="emails/",
            template_suffix="html",
            recipient_list=recipient_list,
            context={
                "recipient_email_text": ", ".join(recipient_list),
                "image_url": "http://localhost:8000/media/product/images/sample.png"
            },
        )
    
    except Exception as e:
        raise e
        print("Error sending templated email:", str(e), e)
        


def send_sample_email():
    try:
        message = EmailMessage(
            subject="Test Email from Storefront",
            body="This is a test email sent from the Storefront application.",
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
            to=["admin@storefront.com"])
        message.attach_file('media/product/images/sample.png')
        message.send()
    except ValueError:
        print("Invalid header found while sending email.")

def say_goodbye_to_my_project(request):
    goodbye_message = "Goodbye from Project app! See you again!"
    notify_customers.delay('hello')
    # send_template_mail()
    # send_sample_email()
    # mail_admins(
    #     subject="Goodbye from Storefront",
    #     message="goodbye",
    #     html_message="A user has just said goodbye from the Project app view.")
    return render(request, 'bye.html', {'goodbye_message': goodbye_message})








# Create your views here.


def say_hello_to_my_project(request):
    query_set = Product.objects.filter(Q(name__icontains="coffee") | Q(unit_price__gte=20, inventory__gte=25))
    products = list(Product.objects.filter(unit_price__gt=F('inventory')))

    customer_query_set = Customer.objects.select_related('user').annotate(
        full_name=Func(F('user__first_name'), F('user__last_name'), function="CONCAT_WS", template="%(function)s(' ',%(expressions)s)"),
        full_name_without_func=Concat('user__first_name', Value(' '), 'user__last_name')
    )
    print(list(customer_query_set))
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
    last_5_orders = Order.objects.select_related('customer').prefetch_related('items__product').order_by('-placed_at')[:5]
    return render(request, 'orders.html', {'orderitems': last_5_orders})

def aggregate_example(request):
    result = Product.objects.aggregate(
        total_inventory_count = Sum('inventory'),
        min_price = Min('unit_price'),
        max_price = Max('unit_price'),
        total_products = Count('id'),
        avg_price = Avg('unit_price')
    )
    return get_data_from_contenttype_example(request)
    return render(request, 'aggregate.html', {'result': result, 'name': 'Products'})

def get_data_from_contenttype_example(request):
    query_set = TaggedItem.objects\
                        .get_tag_items_for_obj_type(Product, object_id=1) \
                          .select_related('tag') \
                          
    return render(request, 'aggregate.html', {'tags': list(query_set), 'name': 'Content Type'})