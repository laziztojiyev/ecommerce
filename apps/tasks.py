import time

from celery import shared_task


@shared_task
def add(x):
    time.sleep(3)
    return f'OK{x}'




