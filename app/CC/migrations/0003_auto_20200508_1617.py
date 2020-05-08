# Generated by Django 3.0.6 on 2020-05-08 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CC', '0002_auto_20200507_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='url',
            new_name='URL_keyword',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='CC.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ManyToManyField(to='CC.Image'),
        ),
    ]
