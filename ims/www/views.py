from django.shortcuts import render, redirect
from .models import Item, BulkItem, Consumable, License
from .forms import AddItemForm

# Create your views here.
def homeView(request):
    context = {
        "title":"Dashboard",
        "items": Item.objects.all(),
    }
    return render(request,"dashboard.html", context)


# Single Items
def items(request):
    context = {
        "title":"Items",
        "items": Item.objects.all(),
    }
    return render(request, 'items.html', context)


# function for adding new Item to DB
def add_item(request):
    if request.method=="POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
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



# For Accessories
def bulk_items(request):
    context = {
        "title":"Accessories",
        "items": BulkItem.objects.all(),
    }
    return render(request, 'items_bulk.html', context)
