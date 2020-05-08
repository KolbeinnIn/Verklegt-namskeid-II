from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True, blank=True)
    URL_keyword = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)

    def _get_full_name(self, category):
        if category.parent_id != None:
            string = self._get_full_name(category.parent)
            string += ' > ' + category.name
            return string
        else:
            return category.name

    def __str__(self):
        return self._get_full_name(self)

    def __lt__(self, other):
        return self.name < other.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    relative_path = models.CharField(max_length=1024)


class Product(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    P_EAN = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    discount = models.FloatField(default=0, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    status = models.BooleanField(default=True, blank=True)
    category = models.ManyToManyField(Category)
    image = models.ManyToManyField(Image)
    def __str__(self):
        return self.name