from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "CC/index.html", context={"listi": {999: "vara1", 2: "vara2", 3: "vara3", 4: "vara4", }})




