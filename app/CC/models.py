from django.db import models


class URL:
    def __init__(self):
        self.replace_arr = [('á', 'a'), ('ð', 'd'), ('ö', 'o'), ('ó', 'o'), ('í', 'i'), ('ý', 'y'), ('ó', 'o'),
                            ('æ', 'ae'), ('ø', 'o'), ('ú', 'u'), ('þ', 'th'), ('é', 'e')]
        self.replace_with_dash = ['/', '\\', ' ', '*', '+', '=', '\n', '\r', '\t']
        self.replace_with_empty = ['%', '&', "'", '"', '(', ')', ',', '.']

    # Make sure the url does not exist. Adds number if url already exists
    def _does_url_exist_questionmark(self, url):
        categories = Category.objects.all()
        products = Product.objects.all()
        i = 0
        while True:
            not_changed = True
            # TODO Breyta forloops í function
            for category in categories:
                if url == category.URL_keyword:
                    i += 1
                    if i > 1:
                        url = url[:-1] + str(i)
                    else:
                        url += "-" + str(i)
                    not_changed = False
                    break
            if not_changed:
                for product in products:
                    if url == product.URL_keyword:
                        i += 1
                        if i > 1:
                            url = url[:-1] + str(i)
                        else:
                            url += "-" + str(i)
                        not_changed = False
                        break
            if not_changed:
                break
        return url

    def _make_url(self, name):
        url = name.lower()
        # Replace symbols and icelandic letters
        for x in self.replace_arr:
            url = url.replace(x[0], x[1])
        for i in self.replace_with_dash:
            url = url.replace(i, '-')
        for y in self.replace_with_empty:
            url = url.replace(y, '')
        url = self._does_url_exist_questionmark(url)
        return url


class Category(models.Model, URL):
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

    def check_url(self):
        if self.URL_keyword != None:
            self.URL_keyword = self._make_url(self.name)
        else:
            self.URL_keyword = self._make_url(self.name)
        self.save()

    def __str__(self):
        return self._get_full_name(self)

    def __lt__(self, other):
        return self.name < other.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    relative_path = models.CharField(max_length=1024)


class Product(models.Model, URL):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, blank=True)
    URL_keyword = models.CharField(max_length=255, blank=True)
    P_EAN = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    discount = models.FloatField(default=0, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    status = models.BooleanField(default=True, blank=True)
    category = models.ManyToManyField(Category)
    image = models.ManyToManyField(Image)

    def check_url(self):
        if self.url != None:
            self.url = self._make_url(self.name)
        else:
            self.url = self._make_url(self.name)
        self.save()

    def __str__(self):
        return self.name
