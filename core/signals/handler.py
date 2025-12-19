from django.dispatch import receiver
from store.signals import order_created


@receiver(signal=order_created)
def on_order_created(sender, **kwargs):
    current_order = kwargs.get('current_order')
    print(f"Order created with ID: {current_order.id} for Customer ID: {current_order.customer.id}")