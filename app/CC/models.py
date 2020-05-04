from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    URL_keyword = models.CharField(max_length=255, blank=True)
    parent_id = models.ForeignKey('self', on_delete=models.DO_NOTHING)

class Image(models.Model):
    name = models.CharField(max_length=255)
    relative_path = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    P_EAN = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    discount = models.FloatField(default=0)
    description = models.CharField(max_length=1024, blank=True)
    status = models.BooleanField(default=True)
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    image_something = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
