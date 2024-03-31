from random import randint

from django.core.mail import send_mail

from apps.models import Category, Product
from root.settings import EMAIL_HOST_USER


def send_welcome_email(emails: list):
    subject = 'Welcome to My Site'
    message = 'Thank you for creating an account!'
    send_mail(subject, message, EMAIL_HOST_USER, emails)
