from django.db import models
from user.models import profile_info


class URL:  # this class exists to make sure that all category and product urls are unique
    # example: if a product is created with the name "Playstation-game" and a product already exists with that name
    # the product will get the URL_keyword/slug playstation-game-1, if that already exists then it will get "playstation-game-2"
    # there also cannot be a category and product with the same slug
    def __init__(self):
        self.replace_arr = [('á', 'a'), ('ð', 'd'), ('ö', 'o'), ('ó', 'o'), ('í', 'i'), ('ý', 'y'), ('ó', 'o'),
                            ('æ', 'ae'), ('ø', 'o'), ('ú', 'u'), ('þ', 'th'), ('é', 'e')]
        self.replace_with_dash = ['/', '\\', ' ', '*', '+', '=', '\n', '\r', '\t']
        self.replace_with_empty = ['%', '&', "'", '"', '(', ')', ',', '.']

    # Make sure the url does not exist. Adds number if url already exists
    def _does_url_exist_questionmark(self, url, id):
        categories = Category.objects.all()
        products = Product.objects.all()
        i = 0
        while True:
            not_changed = True
            for category in categories:
                if int(id) != category.id:
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
                    if int(id) != product.id:
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

    def _make_url(self, name, id):
        url = name.lower()
        # Replace symbols and icelandic letters
        for x in self.replace_arr:
            url = url.replace(x[0], x[1])
        for i in self.replace_with_dash:
            url = url.replace(i, '-')
        for y in self.replace_with_empty:
            url = url.replace(y, '')
        url = self._does_url_exist_questionmark(url, id)
        return url


class Category(models.Model, URL):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True, blank=True)
    URL_keyword = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    def _get_full_name_rec(self, category):
        if category.parent_id is not None:
            string = self._get_full_name_rec(category.parent)
            string += ' > ' + category.name
            return string
        else:
            return category.name

    def _get_full_name(self):
        self.full_name = self._get_full_name_rec(self)
        self.save()

    def check_url(self):
        if self.URL_keyword == "":
            self.URL_keyword = self._make_url(self.name, self.id)
        else:
            self.URL_keyword = self._make_url(self.URL_keyword, self.id)
        self.save()

    def __str__(self):
        if self.full_name is None:
            self._get_full_name()
        return self.full_name

    def __lt__(self, other):
        return self.name < other.name

    def initialize(self):
        self.check_url()
        self._get_full_name()
        self.save()


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
    total = models.IntegerField(blank=True, null=True)

    def calculate_total(self):
        self.total = self.price * ((100 - self.discount)/100)

    def check_url(self):
        if self.URL_keyword == "":
            self.URL_keyword = self._make_url(self.name, self.id)
        else:
            self.URL_keyword = self._make_url(self.URL_keyword, self.id)
        self.save()

    def __str__(self):
        return self.name

    def initialize(self):  # checks if the url is unique, if not, fix it
        self.check_url()
        self.calculate_total()  # calculates the total from price and discount
        self.save()  # saves product to database


class Cart(models.Model):
    session_id = models.CharField(max_length=999, blank=True, null=True)
    person_info = models.ForeignKey(profile_info, on_delete=models.DO_NOTHING, blank=True, null=True)
    shipping = models.CharField(max_length=50)


class CartItem(models.Model):
    prod_id = models.IntegerField(default=-1)
    prod_name = models.CharField(max_length=255, default="")
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)


class Order(models.Model):
    total = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
