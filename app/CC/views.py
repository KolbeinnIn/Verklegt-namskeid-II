from django.shortcuts import render
from CC.models import Product


def index(request):
    return render(request,
                  "CC/index.html",
                  context={
                      "prod_list": Product.objects.all()[:6]
                  })
