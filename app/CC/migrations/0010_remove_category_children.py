# Generated by Django 3.0.6 on 2020-05-13 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CC', '0009_cart_cartitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='children',
        ),
    ]
