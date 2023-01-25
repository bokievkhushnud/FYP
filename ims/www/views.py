from django.shortcuts import render, redirect
from .models import Item, BulkItem, Consumable, License, Category, Department
from .forms import AddItemForm, AddBulkItemForm, AddConsumableForm, AddLicenseForm
from django.db.models import Q
from datetime import datetime


# Create your views here.


def homeView(request):
    context = {
        "title": "Dashboard",
        "items": Item.objects.all(),
    }
    return render(request, "dashboard.html", context)


# ------------------------------ ITEMS ------------------------------------------------


# Single Items

def items(request):

    category = request.GET.get("category")
    department = request.GET.get("department")
    status = request.GET.get("status")
    date_received = request.GET.get("date_recieved")
    q = request.GET.get("q")

    search_filters = {
        "category": category if category is not None else "",
        "department": department if department is not None else "",
        "status": status if status is not None else "",
        "date_recieved": date_received if date_received is not None else "",
        "q": q if q is not None else "",
    }
    items_list = Item.objects.filter(
        Q(category__name__contains=search_filters["category"]) &
        Q(department__name__contains=search_filters["department"]) &
        Q(status__contains=search_filters["status"]) &
        Q(date_received__contains=search_filters["date_recieved"])
    ).filter(
        Q(item_code__contains=search_filters["q"]) |
        Q(item_name__contains=search_filters["q"]) |
        Q(location__contains=search_filters["q"]) |
        Q(description__contains=search_filters["q"]) |
        Q(holder__contains=search_filters["q"]) |
        Q(notes__contains=search_filters["q"]) |
        Q(vendor__contains=search_filters["q"])
    )

    context = {
        "title": "Items",
        "items": items_list,
        "total_count": items_list.count(),
        "broken_count": items_list.filter(status="broken").count(),
        "available_count": items_list.filter(status="available").count(),
        "inuse_count": items_list.filter(status="outinuse").count(),
        "categories": Category.objects.all(),
        "departments": Department.objects.all(),
        "search_filters": search_filters
    }
    return render(request, 'items/items.html', context)


# function for adding new Item to DB
def add_item(request):
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('items')

    context = {
        "title": "Add New Item",
        "form": AddItemForm(),
    }
    return render(request, "items/add_new_item.html", context)


# function for item details
def item_detail(request, pk):

    item = Item.objects.get(id=pk)

    context = {
        "title": f"{item.item_name} Detail",
        "item": item,
    }

    return render(request, "items/item_detail.html", context)

# ----------------------------------------- BULK ITEMS -----------------------------------

# For Accessories


def bulk_items(request):
    context = {
        "title": "Accessories",
        "items": BulkItem.objects.all(),
    }
    return render(request, 'accessories/items_bulk.html', context)


# Function for Accessories details
def buik_item_detail(request, pk):
    item = BulkItem.objects.get(id=pk)
    context = {
        "title": f"{item.name} Detail",
        "item": item,
    }
    return render(request, "accessories/bulkitem_detail.html", context)


# Function for adding new Accessory to DB
def add_bulkitem(request):
    if request.method == "POST":
        form = AddBulkItemForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('accessories')

    context = {
        "title": "Add New Accessories",
        "form": AddBulkItemForm(),
    }
    return render(request, "accessories/add_new_accessories.html", context)


# ------------------------------------------ CONSUMABLES -------------------------------------

# For consumables
def consumables(request):
    context = {
        "title": "Consumables",
        "items": Consumable.objects.all(),
    }
    return render(request, 'consumables/consumables.html', context)


# Function for consumables details
def consumables_detail(request, pk):
    item = Consumable.objects.get(id=pk)
    context = {
        "title": f"{item.name} Detail",
        "item": item,
    }
    return render(request, 'consumables/consumable_detail.html', context)


# Function for adding new consumables to DB
def add_consumables(request):
    if request.method == "POST":
        form = AddConsumableForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('consumables')

    context = {
        "title": "Add Consumables",
        "form": AddConsumableForm(),
    }
    return render(request, 'consumables/add_new_consumables.html', context)


# ----------------------------------------------- Licenses --------------------------

# For consumables
def licenses(request):
    context = {
        "title": "Licenses",
        "items": License.objects.all(),
    }
    return render(request, 'license/licenses.html', context)


# Function for consumables details
def licenses_detail(request, pk):
    item = License.objects.get(id=pk)
    context = {
        "title": f"{item.license_name} Detail",
        "item": item,
    }
    return render(request, 'license/license_detail.html', context)


# Function for adding new consumables to DB
def add_licenses(request):
    if request.method == "POST":
        form = AddLicenseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('licenses')

    context = {
        "title": "Add License",
        "form": AddLicenseForm(),
    }
    return render(request, 'license/add_new_license.html', context)


# Bulk Delete
def delete_items(request):
    if request.method == "POST":
        checked_items = request.POST.getlist("item_id")
        if len(checkout_items)>0:
            Item.objects.filter(id__in=checked_items).delete()
        return redirect('items')


# Buck Checkout
def checkout_items(request):
    if request.method == "POST":
        checked_items = request.POST.getlist("item_id")
        print(checked_items)
