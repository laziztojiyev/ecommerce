from django.db import models
from django.db.models import DateTimeField


# # Create your models here.
class BaseModel(models.Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True