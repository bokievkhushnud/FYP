from django.shortcuts import render, redirect
from django.conf import settings
from qrcode import *
from .models import Item, GeberatedQRCode
from .forms import AddItemForm

# Create your views here.
def homeView(request):
    context = {
        "title":"Dashboard",
        "items": Item.objects.all(),
    }
    return render(request,"dashboard.html", context)


# function to generate QR code for every item
def generate_qr(data,id):
    img = make(data)
    img_name = 'qr'+str(id)+ '.png'
    img_url = settings.MEDIA_ROOT + 'qrcode/' + img_name
    img.save(img_url)
    return img_name


# function for adding new Item to DB
def add_item(request):

    if request.method=="POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        data = f'item_detail/{new_item.id}'
        img_url  = generate_qr(data,new_item.id)
        new_qr = GeberatedQRCode(item = new_item, qr_code_url = img_url)
        new_qr.save()
        return redirect('home')
    
    
    context = {
        "title":"Add New Item",
        "form": AddItemForm(),
    }

    return render(request,"add_new_item.html", context)



# function for item details
def item_detail(request,pk):

    item = Item.objects.get(id=pk)

    context = {
        "title":f"{item.item_name} Detail",
        "item": item,
    }

    return render(request,"item_detail.html", context)
