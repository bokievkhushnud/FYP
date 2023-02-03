from django.shortcuts import render, redirect
from .models import Item, License, Category, Department
from .forms import AddItemForm, AddAccessoryForm, AddConsumableForm, AddLicenseForm, CustomUserCreationForm
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .utils import generate_code, generate_qr

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
    status = request.GET.get("status")
    item_type = request.GET.get("item_type")
    date_received = request.GET.get("date_recieved")
    q = request.GET.get("q")

    search_filters = {
        "category": category if category is not None else "",
        "status": status if status is not None else "",
        "item_type": item_type if item_type is not None else "",
        "date_recieved": date_received if date_received is not None else "",
        "q": q if q is not None else "",
    }
    items_list = Item.objects.filter(
        Q(category__name__contains=search_filters["category"]) &
        Q(status__contains=search_filters["status"]) &
        Q(item_type__contains=search_filters["item_type"]) &
        Q(date_received__contains=search_filters["date_recieved"])
    ).filter(
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
        "total_count": Item.objects.count(),
        "broken_count": Item.objects.filter(status="broken").count(),
        "available_count": Item.objects.filter(status="available").count(),
        "inuse_count": Item.objects.filter(status="outinuse").count(),
        "categories": Category.objects.all(),
        "search_filters": search_filters
    }
    return render(request, 'items/items.html', context)


# function for adding new Item to DB
def add_item(request):
    department = Department.objects.get(head=request.user)
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(name=request.POST.get("category"))
            item.category = cat[0]
            item.department = department
            item.item_type = "asset" 
            item.save()

        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
        return redirect('items')
    context = {
        "title": "Add New Item",
        "categories": Category.objects.filter(department=department),
        "form": AddItemForm(),
    }
    return render(request, "items/add_new_item.html", context)


def add_accessory_consumables(request):
    department = Department.objects.get(head=request.user)
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(name=request.POST.get("category"))
            item.category = cat[0]
            item.department = department
            item.item_type = "asset" 
            item.save()

        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
        return redirect('items')
    context = {
        "title": "Add New Item",
        "categories": Category.objects.filter(department=department),
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
        if len(checkout_items) > 0:
            Item.objects.filter(id__in=checked_items).delete()
        return redirect('items')


# Buck Checkout
def checkout_items(request):
    if request.method == "POST":
        checked_items = request.POST.getlist("item_id")
        print(checked_items)


# Registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                messages.success(request, 'Account created successfully')
                return redirect('home')
            except Exception as e:
                print(e)
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form, "title": "Registration", })
