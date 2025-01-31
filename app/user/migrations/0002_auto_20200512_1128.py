# Generated by Django 3.0.6 on 2020-05-12 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile_info',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile_info',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile_info',
            name='image_path',
            field=models.CharField(blank=True, max_length=9999, null=True),
        ),
        migrations.AlterField(
            model_name='profile_info',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
