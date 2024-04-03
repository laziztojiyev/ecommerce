from django.db import models
from django.db.models import CharField, DateTimeField, ForeignKey, CASCADE, ImageField, PositiveIntegerField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.models import BaseModel


class Category(MPTTModel, BaseModel):
    name = CharField(max_length=255, unique=True)
    image = ImageField(upload_to='media/categories', null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'{self.name}'

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'kategoriya'
        verbose_name_plural = 'kategoriyalar'


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
    name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    product = ForeignKey('apps.Product', CASCADE)
    quantity = PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'buyurtma'
        verbose_name_plural = 'buyurtmalar'

    @property
    def remove_quantity(self):
        if self.product.quantity >= self.quantity:
            self.product.quantity -= self.quantity
            return self.quantity
        else:
            return f'omborda {self.product.quantity} ta mahsulot bor'


class SiteSettings(BaseModel):
    shipping_change = PositiveIntegerField()

    class Meta:
        verbose_name = 'Sahifa sozlamasi'
        verbose_name_plural = 'Sahifa sozlamalari'

    def __str__(self):
        return f'yetkazib berish - {self.shipping_change}'
