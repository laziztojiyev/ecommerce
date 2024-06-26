from django.db import models
from django.db.models import (Model, CharField, DateTimeField,
                              ForeignKey, CASCADE, ImageField,
                              PositiveIntegerField, SlugField)
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.text import slugify

from apps.models import BaseModel


class Category(MPTTModel, BaseModel):
    name = CharField(max_length=255, unique=True)
    image = ImageField(upload_to='media/categories', null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = SlugField(max_length=255, null=True, blank=True, editable=False)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.name}'

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'kategoriya'
        verbose_name_plural = 'kategoriyalar'

        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_slug')
        ]


class Wishlist(BaseModel):
    user = ForeignKey('users.CustomUser', CASCADE)
    product = ForeignKey('apps.Product', CASCADE, 'wishlists')
    added_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = 'sevimli'
        verbose_name_plural = 'sevimlilar'


class Cart(BaseModel):
    user = ForeignKey('users.CustomUser', CASCADE)
    product = ForeignKey('apps.Product', CASCADE, 'products')
    quantity = PositiveIntegerField(default=1)
    added_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} ning savatida: {self.product.name} x {self.quantity}'

    class Meta:
        verbose_name = 'savatcha'
        verbose_name_plural = 'savatchalar'


class Order(BaseModel):
    class Status(models.TextChoices):
        NEW = 'yangi'
        READY = 'dostavkaga tayyor'
        DELIVERING = 'yetkazilmoqda'
        DELIVERED = 'yetkazib berildi'
        ARCHIVE = 'arxivlandi'
        CANCELLED = 'bekor qilindi'
        BROKEN = 'nosoz'
        ARRIVED = 'qaytib keldi'
        WAITING = 'keyin oladi'

    name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    product = ForeignKey('apps.Product', CASCADE)
    quantity = PositiveIntegerField(default=1)
    status = CharField(max_length=55, choices=Status, default=Status.NEW)

    class Meta:
        verbose_name = 'buyurtma'
        verbose_name_plural = 'buyurtmalar'


class SiteSettings(BaseModel):
    shipping_change = PositiveIntegerField()

    class Meta:
        verbose_name = 'Sahifa sozlamasi'
        verbose_name_plural = 'Sahifa sozlamalari'

    def __str__(self):
        return f'yetkazib berish - {self.shipping_change}'


class Threads(Model):
    name = CharField(max_length=255)
    user = ForeignKey('users.CustomUser', CASCADE, related_name='threads')
    product = ForeignKey('apps.Product', CASCADE)

    class Meta:
        verbose_name = 'oqim'
        verbose_name_plural = 'oqimlar ro"yxati'

    def __str__(self):
        return f'{self.product.name} --> {self.user}'
