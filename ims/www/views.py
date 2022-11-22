from django.shortcuts import render, HttpResponse

# Create your views here.


def homeView(request):
    return HttpResponse("Hello")