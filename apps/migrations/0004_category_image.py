# Generated by Django 5.0.2 on 2024-03-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_remove_product_shipping_cost_product_site_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/categories'),
        ),
    ]
