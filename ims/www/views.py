from django.shortcuts import render
from django.conf import settings
from qrcode import *
import time

# Create your views here.


def homeView(request):
    
    context = {
        "title":"Dashboard"
    }
    return render(request,"dashboard.html", context)

def add_item(request):
    if request.method=="POST":
        data = request.POST['url']
        img = make(data)
        img_name = 'qr' + str(time.time()) + '.png'
        img.save(settings.MEDIA_ROOT + 'qrcode/' + img_name)
        return render(request, 'home.html', {'img_name': img_name})
    
    context = {
        "title":"Add New Item"
    }
    return render(request,"add_new_item.html", context)


