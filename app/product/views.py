from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, "product/index.html", context={"quantity":100 ,"title":"Ég er vara","price":22000,"image":"logo", "amount":1, "description":"This is the very cool description."})