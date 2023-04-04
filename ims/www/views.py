from django.db.models.query_utils import Q
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Item, License, Category, Department, ItemAssignment, Profile
from .forms import AddItemForm, AddAccessoryForm, AddLicenseForm, CustomUserCreationForm, PasswordResetForm, SetPasswordForm, ProfileForm
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date
from .tokens import account_activation_token
import re
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from datetime import date
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.db.models import Count,Sum
from django.db.models.functions import TruncMonth,ExtractYear
import datetime
# Create your views here.


def homeView(request):
    items = Item.objects.all()
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    data = [10, 20, 30, 40, 50, 60, 70]
    items_with_year = Item.objects.annotate(year=ExtractYear('date_received')).values('year').distinct()
    years = [item['year'] for item in items_with_year]
    # Prepare the data for the Category chart
    categories = Category.objects.all().annotate(total_quantity=Sum('item__quantity'))
    category_names = [category.name for category in categories]
    item_quantities = [category.total_quantity if category.total_quantity else 0 for category in categories]
    # Prepare data for Item Types chart
    item_types_data = (
        items.values('item_type')
        .annotate(item_count=Sum('quantity'))
        .order_by('item_type')
    )
    type_label = [types['item_type'] for types in item_types_data]
    type_data = [types['item_count'] if types['item_count'] else 0 for types in item_types_data]


    broken_items = items.filter(status='broken')
    recently_checked_out_items = ItemAssignment.objects.filter(department= items[0].department, action="assign")
    context = {
        "title": "Dashboard",
        "available_count": items.filter(status='available').count(),
        "checked_out_count":items.filter(status='outinuse').count(),
        "broken_count":broken_items.count(),
        "total_count": items.all().count(),
        "recently_checked_out_items":recently_checked_out_items.order_by('-date')[:10],
        "broken_items":broken_items[:10],
        "items_in_shortage":items.filter(Q(item_type="accessory")|Q(item_type="consumable")).order_by("quantity")[:10],
        "items_due_return":recently_checked_out_items.order_by("due_date")[:10],
        'labels': labels,
        'data': data,
        "category_names":category_names,
        'item_quantities':item_quantities,
        'type_label':type_label,
        'type_data':type_data,
        'years':years,
        
    }
    return render(request, "dashboard.html", context)




def get_monthly_added_items_data(request,year):
    monthly_data = (
        Item.objects.filter(date_received__year=year)
        .annotate(month=TruncMonth('date_received'))
        .values('month')
        .annotate(items_added=Count('id'))
        .order_by('month')
    )
    months = [data['month'].strftime('%B') for data in monthly_data]
    items_added = [data['items_added'] for data in monthly_data]

    data = {
        'months': months,
        'items_added': items_added,
    }

    return JsonResponse(data)

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
    item = Item.objects.get(id=pk)

    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(
                name=request.POST.get("category"))
            item.category = cat[0]
            item.save()
            messages.success(request, 'Item Edited !')
            return redirect('item_detail', pk)

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
        "item": item,
    }
    return render(request, "items/update_item.html", context)


def update_consumables(request, pk):
    department = Department.objects.get(head=request.user)
    item = Item.objects.get(id=pk)

    if request.method == "POST":
        form = AddAccessoryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            cat = Category.objects.filter(department=department).filter(
                name=request.POST.get("category"))
            item.category = cat[0]
            item.save()
            messages.success(request, 'Item Edited !')
            return redirect('item_detail', pk)

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
        "item": item,
    }
    return render(request, "items/update_consumable.html", context)


# function for item details
def item_detail(request, pk):

    item = Item.objects.get(id=pk)
    checked_out_items = ItemAssignment.objects.filter(
        item=item, action="assign")

    context = {
        "title": f"{item.item_name} Detail",
        "item": item,
        "history": checked_out_items,

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
        if item.min_alert_quantity>0:
            if item.quantity<=item.min_alert_quantity:
                email = EmailMessage(
                    f"{item}:Items in Shortage", f"Dear Admin, the following item is in shortage:\n{item}\t{item.quantity} available", to=[item.department.head.email])
                email.send()
        # create new Assignment
        item_out = ItemAssignment(
            item=item,
            quantity=quantity,
            action="assign",
            department=department,
            location=location,
            requestor=requestor,
            done_by=done_by,
            due_date=due_date,
            notes=notes,
        )
        item_out.save()
        email = EmailMessage(
            f"{item}", f"Dear {requestor.first_name},\nNew Items was assigned to you:\n{item}----{quantity}---{location}---{due_date}\nNotes: {notes}\nBy: {done_by} at {date}", to=[requestor.email])
        email.send()
        
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
            if item.status!='broken':
                item.status = "available"
        else:
            if int(item.quantity)+int(quantity) > 0:
                item.status = "available"
            item.quantity = int(item.quantity)+int(quantity)
        item.save()

        # create new Assignment
        ItemAssignment.objects.filter(id=pk).update(
            item=item,
            quantity=quantity,
            action="return",
            location=location,
            requestor=requestor,
            done_by=done_by,
            due_date=due_date,
            notes=notes,
        )

        # Redirect
        email = EmailMessage(
            f"{item}", f"Dear {requestor.first_name},\nItem was returned:\n{item}----{quantity}\nNotes: {notes}\nBy: {done_by}", to=[requestor.email])
        email.send()
        messages.success(request, 'Checked In Successfully')
        return redirect("item_detail", item.id)

    # users = User.objects.all()
    context = {
        "item": assingment,
        "today": date.today()
    }
    return render(request, "items/checkin.html", context)

# item broken view: To report the item is broken
def item_outoforder(request,pk):
    item =Item.objects.get(id = pk)
    item.status = "broken"  
    item.save()
    email = EmailMessage(
            f"{item} Out of Order", f"Report: {item} is out of order\nLocation: {item.location}.",to=[item.department.head.email])
    email.send()
    messages.success(request, 'Report sent to Admin successfully!')
    return redirect("item_detail", item.id)


# item fixed view
def item_fixed(request,pk):
    item =Item.objects.get(id = pk)
    if item.location == 'storage':
        item.status = "available"
    else:
        item.status = "outinuse"
    item.save()
    messages.success(request, 'Report sent to Admin successfully!')
    return redirect("item_detail", item.id)

# PDF of qr codes 
def generate_pdf(request):
    if request.method == "POST":
        checked_items = request.POST.getlist("item_id")
        size = request.POST.get("size")
        gap = request.POST.get("gap")
        mx = request.POST.get("mx")
        my = request.POST.get("my")
        # Create a file-like buffer to receive PDF data.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="qrcodes.pdf"'
        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response, pagesize=A4, bottomup=1)
        # p.setPageRotation(180)
        items = Item.objects.filter(id__in=checked_items)
        # image_paths =  [(settings.MEDIA_ROOT + 'qrcode/' + items) for i in range(100) ]
        # Define a list of image paths
        image_paths = list(
            map(lambda item: settings.MEDIA_ROOT + 'qrcode/' + item.qr_code, items))
        image_width = int(size)
        image_height = int(size)
        padding = int(gap)
        p.translate(0, A4[1]-image_height)
        x = 0+int(mx)
        y = 0-int(my)

        for i in range(len(image_paths)):

            image = ImageReader(image_paths[i])
            p.drawImage(image, x, y, width=image_width,
                        height=image_height, showBoundary=True)

            x += (image_width+padding)
            if (x+image_width+padding+int(mx)) > A4[0]:
                if (y-(2*image_height+padding+int(my))) <= -A4[1]:
                    p.showPage()
                    p.translate(0, A4[1]-image_height)
                    x = 0+int(mx)
                    y = 0-int(my)
                else:
                    y -= (image_height+padding)
                    x = 0+int(mx)

        p.showPage()
        # Close the PDF object cleanly, and we're done.
        p.save()

        return response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="qrcodes.pdf"'
    return response


def print_qr(request, pk=None):
    checked_items = request.POST.getlist("item_id")
    if pk is not None:
        checked_items.append(pk)
    context = {
        "items": Item.objects.filter(id__in=checked_items),
        "all_items": Item.objects.all().exclude(id__in=checked_items),
    }

    return render(request, "items/print_qrcodes.html", context)


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('auth/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request, f'Dear user, please check your inbox and click on activation link to confirm and complete the registration. Check your spam folder!')
    else:
        messages.error(
            request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


# Registration
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        if not re.match(r'^[a-zA-Z]+\.[a-zA-Z]+(_\d{4})?@ucentralasia\.org$', email):
            messages.error(request, 'Please enter a valid UCA email address.')
            return redirect("register")

        first_name, last_name = email.split('@')[0].split('.')
        if "_" in last_name:
            last_name = last_name.split("_")[0]
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.username = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            # need to change to be redirected the special page
            return redirect('home')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form, "title": "Registration", })


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        email = EmailMessage(
            "Accaunt Created", f"Dear {user.first_name},\nYour accaunt is creataed successfully", to=[user.email])
        email.send()
        messages.success(
            request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')


def auth(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, "auth/login.html")


def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            email = EmailMessage(
            "Password Changed", f"Dear {user.first_name},\nYour password is changed successfully", to=[user.email])
            email.send()
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'auth/recover_password.html', {'form': form})


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("auth/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[
                                     associated_user.email])
                if email.send():
                    messages.success(request,
                                     """
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        """
                                     )
                else:
                    messages.error(
                        request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('home')

    form = PasswordResetForm()
    return render(request, "auth/forgot_password.html", context={"form": form})


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                email = EmailMessage(
                    "Password  reset", f"Dear {user.first_name},\nYour password is reset successfully", to=[user.email])
                email.send()
                messages.success(
                    request, "Your password has been set. You may go ahead and log in  now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'auth/recover_password.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(
        request, 'Something went wrong')
    return redirect("home")


def profilePage(request):
    profile = Profile.objects.get(owner=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print("It is valid")
            form.save()
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    context = {
        'title': 'Profile',
        'profile': profile,
        'items': ItemAssignment.objects.filter(requestor=request.user),
        'form': ProfileForm(instance=profile)
    }
    return render(request, 'profile.html', context)


def reportPage(request):
    category = request.GET.get("category")
    owner = request.GET.get("owner")
    status = request.GET.get("status")
    item_type = request.GET.get("item_type")
    date_received = request.GET.get("date_recieved")
    date_received_to = request.GET.get("date_recieved_to")    
    search_filters = {
        "category": category if category is not None else "",
        "owner": owner if owner is not None else "",
        "status": status if status is not None else "",
        "item_type": item_type if item_type is not None else "",
        "date_recieved": date_received if date_received is not None else "",
        "date_recieved_to": date_received_to if date_received_to is not None else "",
    }
    items_list = Item.objects.filter(
        Q(category__name__contains=search_filters["category"]) &
        Q(status__contains=search_filters["status"]) &
        Q(item_type__contains=search_filters["item_type"]) 
    )

    if search_filters["date_recieved"]!="":
        items_list = items_list.filter(date_received__gte=search_filters["date_recieved"])
    
    if search_filters["date_recieved_to"]!="":
        items_list = items_list.filter(date_received__lte=search_filters["date_recieved_to"])

    if search_filters["owner"]!="":
        items_list = items_list.filter(holder__username__contains=search_filters["owner"])
    


    context = {
        "title": "reports",
        "items": items_list,
        "total_count": Item.objects.count(),
        "broken_count": Item.objects.filter(status="broken").count(),
        "available_count": Item.objects.filter(status="available").count(),
        "inuse_count": Item.objects.filter(status="outinuse").count(),
        "categories": Category.objects.all(),
        "owners": User.objects.all(),
        "search_filters": search_filters
    }
    return render(request, 'report.html',context )

# download the report 
def download_report(request,type):
    checked_items = request.POST.getlist("item_id")

    items = Item.objects.filter(id__in=checked_items)
    data = {'ID': [item.id for item in items],
            'Name': [item.item_name for item in items],
            'Price': [item.price for item in items],
            'Currency': [item.currency for item in items],
            'Quantity': [item.quantity for item in items],
            'Quantity Unit': [item.quantity_unit for item in items],
            'Category': [item.category for item in items],
            'Department': [item.department for item in items],
            'Item Code': [item.item_code for item in items],
            'Location': [item.location for item in items],
            'Campus': [item.campus for item in items],
            'Date Received': [item.date_received for item in items],
            'Expiration Date': [item.expiration_date for item in items],
            'Order_Number': [item.order_number for item in items],
            'Holder': [[holder.email for holder  in item.holder.all()] for item in items],
            'Status': [item.status for item in items],
            }
    
    df = pd.DataFrame(data)
    if type == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="items.csv"'
        df.to_csv(path_or_buf=response, index=False)
    else:
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename="items.xlsx"'
        df.to_excel(response, index=False, sheet_name='Items')


    return response





