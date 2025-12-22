# from celery import 
from time import sleep
from celery import shared_task

@shared_task
def call_after_delay(*args, **kwargs):
    # sending bulk emails or processing large data can be done here
    print("This function is called after a delay")
    sleep(10)
    print("Delay of 10 seconds is over")
    return "Task Completed"


@shared_task
def notify_customers(*args, **kwargs):
    print("Sending 10k emails to customers...", args, kwargs)
    sleep(10)
    print("All customers have been notified.")
    return "----Notification Task Completed----"