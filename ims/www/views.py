from django.shortcuts import render, redirect
from .models import Item, License, Category, Department, ItemAssignment
from .forms import AddItemForm, AddAccessoryForm, AddLicenseForm, CustomUserCreationForm
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
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


# function for adding new Items to DB
def add_item(request):
    department = Department.objects.get(head=request.user)
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(
                name=request.POST.get("category"))
            item.category = cat[0]
            item.department = department
            item.item_type = "asset"
            item.save()
            messages.success(request, 'Item added successfully')
            return redirect('items')

        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    context = {
        "title": "New Item",
        "categories": Category.objects.filter(department=department),
        "form": AddItemForm(),
    }
    return render(request, "items/add_new_item.html", context)


def add_accessory(request):
    department = Department.objects.get(head=request.user)
    if request.method == "POST":
        form = AddAccessoryForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(
                name=request.POST.get("category"))
            item.category = cat[0]
            item.department = department
            item.item_type = "accessory"
            item.save()
            messages.success(request, 'Item added successfully')
            return redirect('items')

        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    context = {
        "title": "New Accessory",
        "add_url": "add_accessories",
        "categories": Category.objects.filter(department=department),
        "form": AddAccessoryForm(),
    }
    return render(request, "items/add_new_accessory.html", context)


def add_consumable(request):
    department = Department.objects.get(head=request.user)
    if request.method == "POST":
        form = AddAccessoryForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(
                name=request.POST.get("category"))
            item.category = cat[0]
            item.department = department
            item.item_type = "consumable"
            item.save()
            messages.success(request, 'Item added successfully')
            return redirect('items')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    context = {
        "title": "New Consumable",
        "categories": Category.objects.filter(department=department),
        "add_url": "add_consumables",
        "form": AddAccessoryForm(),
    }
    return render(request, "items/add_new_accessory.html", context)


def update(request, pk):
    department = Department.objects.get(head=request.user)
    item = Item.objects.get(id = pk)

    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(
                name=request.POST.get("category"))
            item.category = cat[0]
            item.save()
            messages.success(request, 'Item Edited !')
            return redirect('items')

        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    context = {
        "title": "Edit Item",
        "categories": Category.objects.filter(department=department),
        "form": AddItemForm(instance=item),
        "item":item,
    }
    return render(request, "items/update_item.html", context)



def update_consumables(request, pk):
    department = Department.objects.get(head=request.user)
    item = Item.objects.get(id = pk)

    if request.method == "POST":
        form = AddAccessoryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(
                name=request.POST.get("category"))
            item.category = cat[0]
            item.save()
            messages.success(request, 'Item Edited !')
            return redirect('items')

        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    context = {
        "title": "Edit Item",
        "categories": Category.objects.filter(department=department),
        "form": AddAccessoryForm(instance=item),
        "item":item,
    }
    return render(request, "items/update_consumable.html", context)


# function for item details
def item_detail(request, pk):

    item = Item.objects.get(id=pk)
    checked_out_items = ItemAssignment.objects.filter(item=item, action="assign")

    context = {
        "title": f"{item.item_name} Detail",
        "item": item,
        "history":checked_out_items,

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
def delete_items(request, pk=None):
    if request.method == "POST":
        print("YEESSSS")
        checked_items = request.POST.getlist("item_id")
        print(checkin_items)
        if len(checked_items) > 0:
            Item.objects.filter(id__in=checked_items).delete()
        return redirect('items')
    else:
        Item.objects.filter(id=pk).delete()
        return redirect('items')
        
   



# Check Out
def checkout_items(request, pk):
    # checked_items = request.POST.getlist("item_id");
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = Item.objects.get(id=item_id)
        quantity = request.POST.get("quantity")
        department = item.department
        location = request.POST.get("location")
        requestor_id = request.POST.get("requestor")
        requestor = User.objects.get(id=requestor_id)
        done_by = request.user
        due_date = request.POST.get("due_date")
        notes = request.POST.get("notes")
        item.location = location
        item.holder.add(requestor) 
        if item.item_type == "asset": 
            item.status = "outinuse"
        else:
            if int(item.quantity)-int(quantity) == 0:
                item.status = "outinuse"
            item.quantity = int(item.quantity)-int(quantity)

        
        item.save()

        # create new Assignment 
        item_out = ItemAssignment(
            item=item,
            quantity=quantity,
            action = "assign",
            department=department,
            location=location,
            requestor=requestor,
            done_by=done_by,
            due_date=due_date,
            notes=notes,
        )
        item_out.save()

        messages.success(request, 'Checked Out Successfully')
        return redirect("item_detail", item.id)

        

    users = User.objects.all()
    context = {
        "item": Item.objects.get(id=pk),
        "users": users,
        "today": date.today()
    }
    return render(request, "items/checkout.html", context)


# Check in View
def checkin_items(request, pk):
    # checked_items = request.POST.getlist("item_id");
    assingment = ItemAssignment.objects.get(id=pk)
    if request.method == "POST":
        item = assingment.item
        notes = request.POST.get("notes")
        quantity = assingment.quantity
        location = "storage"
        requestor = assingment.requestor
        done_by = request.user
        due_date = None

        # Change Item in DB
        item.location = location
        item.holder.remove(requestor) 
        if item.item_type == "asset": 
            item.status = "available"
        else:
            if int(item.quantity)+int(quantity) >0:
                item.status = "available"
            item.quantity = int(item.quantity)+int(quantity)
        item.save()

        # create new Assignment 
        ItemAssignment.objects.filter(id=pk).update(
            item=item,
            quantity=quantity,
            action = "return",
            location=location,
            requestor=requestor,
            done_by=done_by,
            due_date=due_date,
            notes=notes,
        )

        # Redirect
        messages.success(request, 'Checked In Successfully')
        return redirect("item_detail", item.id)

    # users = User.objects.all()
    context = {
        "item": assingment,
        "today": date.today()
    }
    return render(request, "items/checkin.html", context)

# Registration


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('home')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form, "title": "Registration", })
