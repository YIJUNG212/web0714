# Generated by Django 4.2.2 on 2023-06-26 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_product_item_price_alter_shopitem_item_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopitem',
            name='item_image_photo',
        ),
    ]