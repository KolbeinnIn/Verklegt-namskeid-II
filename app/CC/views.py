from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "CC/index.html", context={"listi": ["vara1", "vara2", "vara3", "vara4"]})




