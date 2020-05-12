from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "cart/index.html", context={'name': "The big boy with long name", "amount": 1,"price": 22000, "total": 22000})
