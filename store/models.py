from django.db import models

# Create your models here.


MEMBER_SHIP_CHOICES = [
    ('G', 'Gold'),
    ('S', 'Silver'),
    ('B', 'Bronze'),
]



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # Price can be decimal with two decimal places and maximum 3 digits before decimal
    price = models.DecimalField(max_digits=5, decimal_places=2)
    inventory = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBER_SHIP_CHOICES, default=MEMBER_SHIP_CHOICES[2][0])



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