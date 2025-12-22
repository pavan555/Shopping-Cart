import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
app = Celery('storefront')

app.config_from_object('django.conf:settings', namespace="CELERY")


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'project.tasks.notify_customers',
        'schedule': 10,
        'args': (16, 16)
    },

    'call_after_delay': {
        'task': 'project.tasks.call_after_delay',
        'schedule': crontab(minute='*/1'),
        'args': (10, 10)
    }
}

app.conf.timezone = 'UTC'

# for running celery worker and beat, use the following commands: 
# celery -A storefront worker --loglevel=INFO
# celery -A storefront flower -> used to monitor celery tasks
# celery -A storefront beat --loglevel=info
