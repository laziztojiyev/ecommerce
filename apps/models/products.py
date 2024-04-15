from datetime import timedelta

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import CharField, DecimalField, ForeignKey, CASCADE, JSONField, \
    PositiveIntegerField, IntegerField, SlugField
from django.utils.text import slugify
from django.utils.timezone import now
from django_resized import ResizedImageField

from apps.models import BaseModel


class Product(BaseModel):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    slug = SlugField(max_length=255, null=True, blank=True)
    Description = RichTextField()
    category = ForeignKey('apps.Category', CASCADE)
    discount = IntegerField()
    orders = ForeignKey('apps.Order', CASCADE, related_name='orderss')
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

    @property
    def remove_quantity(self):
        if self.quantity >= self.orders.quantity:
            self.quantity -= self.orders.quantity
            return self.quantity
        else:
            return f'omborda {self.quantity} ta mahsulot bor'


class ProductImage(models.Model):
    image = ResizedImageField(size=[1098, 717], upload_to='images/products', null=True, blank=True)
    product = models.ForeignKey('apps.Product', models.CASCADE, related_name='images')

    def __repr__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Mahsulot Rasmi'
        verbose_name_plural = 'Mahsulot Rasmlari'
