from django.db import models

# Create your models here.


MEMBER_SHIP_CHOICES = [
    ('G', 'Gold'),
    ('S', 'Silver'),
    ('B', 'Bronze'),
]

class Promotions(models.Model):
    description = models.CharField(max_length=255)
    discount = models.IntegerField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name="+")

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()
    # Price can be decimal with two decimal places and maximum 3 digits before decimal
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    inventory = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotions, blank=True)



class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBER_SHIP_CHOICES, default=MEMBER_SHIP_CHOICES[2][0])


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    units = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed")
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="customer_orders")

# One to one Relationship example between Customer and Address, if we dont specify primary_key=True in OneToOneField, Django will create an additional id field as primary key
# It results in each customer creating multiple addresses, if we define primary_key=True, it will enforce one to one relationship such that each customer can have only one address
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6, default='500001')
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="customer_address", primary_key=True)



class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

