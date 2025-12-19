from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from store.models import Customer


@receiver(signal=post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_when_user_created(sender, **kwargs):
    user = kwargs['instance']
    created = kwargs['created']

    if created:
        print("Creating customer for user:", user.id, user.username, user.email)
        Customer.objects.create(user=user)

