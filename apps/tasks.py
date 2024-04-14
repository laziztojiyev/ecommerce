import time
from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = "salom bu sizning do'stingiz"
        message = 'tabriklayman siz bizning kanalga azo bo"ldingiz! bizni tugmani bosing va siz a"zo bo"lasiz'
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[to_email],
        )

    return f'Done'
