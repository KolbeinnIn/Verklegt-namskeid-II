from django.contrib.auth.models import User
from django.db import models


class country(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class profile_info(models.Model):
    image_path = models.CharField(max_length=9999)
    phone_nr = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    house_no = models.CharField(max_length=20)
    country = models.ForeignKey(country, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
