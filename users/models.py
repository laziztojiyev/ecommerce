from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField, TextChoices, CharField


# Create your models here.
class CustomUser(AbstractUser):
    class Type(TextChoices):
        USERS = 'users', 'foydalanuvchilar'
        ADMIN = 'admin', 'Admin'
        KURYER = 'kuryer', 'yetkazib beruvchi'
        OPERATOR = 'operator', 'operator'
        MENEGER = 'meneger', 'Menedjer'
    type = CharField(max_length=25, choices=Type.choices, default=Type.USERS)
    image = ImageField(upload_to='images/users', default='1.jpg', null=True, blank=True)
    about_me = RichTextField(null=True, blank=True)
    phone_number = CharField(max_length=25)





