# Function to check if the user is head of some department
def is_department_head(user):
    """
    Function to check if the user 
    is the head of the department or not 
    """
    department = Department.objects.filter(head=user).first()
    return department is not None
# Dashboard View
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def homeView(request):
    """
    This view is for dashboard page,
    It contains, statistics, 
    graphs and tables about 
    the items and categories
    """
    pass
def get_monthly_added_items_data(request, year):
    """
    This view is for Item Added Graph,
    this will recieve the ajax request and
    responcse as json with data, 
    to make the filtering faster.

    """
    pass
# ------------------------------ ITEMS ------------------------------------------------

# Single Items
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def items(request):
    """
    items view is for Items page,
    where it shows, tables with items,
    fillters and search bars

    """
    pass
# function for adding new Items to DB
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def add_item(request):
    """
    View to add new Items (Single items),
    to the db
    """
    pass
# function to add (bulk items)
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def add_accessory(request):
    """
    View to add new Items (bulk items),
    to the db
    """
    pass
# function to add (consumable)
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def add_consumable(request):
    """
    View to add new Items (Consumables),
    to the db
    """
    pass
# function to update assets
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def update(request, pk):
    """
    View to update Assets (single items)
    """
    pass
# function to add bulk items and consumables
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def update_consumables(request, pk):
    """
    View to update consumables and accessories (items in  bulk)
    """
    pass
# function for item details
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def item_detail(request, pk):
    """
    View for detail page of the items
    Where admin can perform, crud operations on items
    plus check in and out
    """
    pass
# Bulk Delete
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
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
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def checkout_items(request, pk):
    """
    This view is for checking out the items
    or assigning items to someone 
    """
    pass
# Check in View
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def checkin_items(request, pk):
    """
    This view is for handling items check in
    or when the items are returned

    """
    pass
# item broken view: To report the item is broken
@login_required(login_url='login/')
def item_outoforder(request, pk):
    item = Item.objects.get(id=pk)
    item.status = "broken"
    item.save()
    subject = f"{item} Out of Order"
    message = f"Report: {item} is out of order\nLocation: {item.location}."
    recipient_list = [item.department.head.email]
    send_email_task.delay(subject, message, recipient_list)

    messages.success(request, 'Report sent to Admin successfully!')
    return redirect("item_detail", item.id)
# item fixed view
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def item_fixed(request, pk):
    item = Item.objects.get(id=pk)
    if item.location == 'storage':
        item.status = "available"
    else:
        item.status = "outinuse"
    item.save()
    messages.success(request, 'Report sent to Admin successfully!')
    return redirect("item_detail", item.id)
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
# PDF of qr codes
def generate_pdf(request):
    """
    View to generate pdf of qr codes and 
    allow customization of the page
    """
    pass
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
# qr code printing page
def print_qr(request, pk=None):
    """
    View to show the print QR codes page
    """
    pass
# function to send an email to the user for confirmation
def activateEmail(request, user, to_email):
    """
    Function to send confirmation email to the user
    """
    pass
# Registration
def register(request):
    """
    View to handle the registration of new users
    """
    pass


# Confirms email and makes the user active
def activate(request, uidb64, token):
    """
    View to active the user account
    """
    pass
# login view
def auth(request):
    """
    Login view, handles the login form and
    redirects accordingly 
    """
    pass
# view to reset the passowrd
def password_reset_request(request):
    """
    This view will send request to reset your password
    by email confirmation
    """
    pass
# View to confirm the email and change the password
def passwordResetConfirm(request, uidb64, token):
    """
    View to confirm the email and change the password
    """
    pass 
# Logout view
def logout_user(request):
    """
    Logout View
    To log out user from the system
    """
    pass
# personal profile page of the users
@login_required(login_url='login/')
def profilePage(request):
    """
    This view is for profile page
    of the users, where they can change their 
    password, profile picture, and see items that are assigned to them
    """
    pass
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
# Page to generate and print reports about the items
def reportPage(request):
    """
    View to generate the report, by using custom filter
    and print or download it in different formats
    such as csv, xls, pdf.

    """
    pass
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def loans(request):
    pass
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def categories(request):
    """
    View for adding new categories
    it should be done only by head of the specific department
    """
    pass
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def categories_update(request, pk):
    """
    View to update category
    """
    pass
@login_required(login_url='login/')
@user_passes_test(is_department_head, login_url='profile/')
def categories_delete(request, pk):
    pass