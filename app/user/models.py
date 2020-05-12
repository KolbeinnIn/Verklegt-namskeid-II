from django.contrib.auth.models import User
from django.db import models


class country(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class profile_info(models.Model):
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    image_path = models.CharField(max_length=9999, blank=True, null=True)
    phone_nr = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    country = models.ForeignKey(country, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

class SearchHistory(models.Model):
    search_query = models.CharField(max_length=999)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
