from celery import shared_task
from django.http import JsonResponse

from users.utils import send_welcome_email


@shared_task
def sending_email(email):
    send_welcome_email([email])
    return JsonResponse({'success': True})
