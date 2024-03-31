from datetime import timedelta

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import CharField, DateTimeField, DecimalField, ForeignKey, CASCADE, ImageField, JSONField, \
    PositiveIntegerField, IntegerField, SlugField, SET_NULL
from django.utils.text import slugify
from django.utils.timezone import now
from django_resized import ResizedImageField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# # Create your models here.
class BaseModel(models.Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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


class Product(BaseModel):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    slug = SlugField(max_length=255, null=True, blank=True)
    Description = RichTextField()
    category = ForeignKey('apps.Category', CASCADE)
    discount = IntegerField()
    characteristics = JSONField(default=dict)
    quantity = PositiveIntegerField(default=0)
    site_settings = ForeignKey('apps.SiteSettings', CASCADE, 'site_settings')

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
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

    class Meta:
        verbose_name = 'mahsulot'
        verbose_name_plural = 'mahsulotlar'
        ordering = ('-created_at',)

    @property
    def is_available(self):
        return self.quantity > 0

    @property
    def discount_price(self):
        return self.price * self.discount / 100

    @property
    def sell_price(self):
        return self.price - self.discount_price

    @property
    def is_new(self):
        return self.created_at >= now() - timedelta(days=2)

    @property
    def add_shipping(self):
        return self.sell_price + 30000


class ProductImage(models.Model):
    image = ResizedImageField(size=[1098, 717], upload_to='images/products', null=True, blank=True)
    product = models.ForeignKey('apps.Product', models.CASCADE, related_name='images')

    def __repr__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Mahsulot Rasmi'
        verbose_name_plural = 'Mahsulot Rasmlari'


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
