# Generated by Django 3.0.6 on 2020-05-13 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20200513_1434'),
        ('CC', '0012_cart_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='person_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.profile_info'),
        ),
    ]
