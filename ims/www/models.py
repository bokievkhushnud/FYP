from django.db import models
from django.contrib.auth.models import User

#  Table for departments
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Table for Categories
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Table for Asset (Single Items)
class Item(models.Model):
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=300)
    price = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=20, default="USD", blank=True)
    location = models.CharField(max_length=100, default="storage", blank=True)
    campus = models.CharField(max_length=20, choices=[("Naryn", "Naryn"), ("Khorog", "Khorog"), ("Tekeli","Tekeli")], default="Naryn")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    vendor = models.CharField(max_length=100, blank=True)
    date_received = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    order_number = models.CharField(max_length=100, blank=True)
    holder = models.CharField(max_length=100, default="", blank=True)
    qr_code = models.CharField(max_length=200, blank=True, default="")
    status = models.CharField(
        max_length=20, choices=[("available", "Available"), ("outinuse", "Out In Use")],
        default="available"
    )

    def __str__(self):
        return self.item_name


# Table for Buik Items 
class BulkItem(models.Model):
    item_code = models.CharField(max_length=20)
    price_per_unit = models.PositiveIntegerField(default=0)
    total_quantity = models.PositiveIntegerField(default=1)
    quantity_unit  = models.CharField(max_length=20, default="PCS")
    total_price = models.PositiveIntegerField(default=0)
    min_alert_quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()
    vendor = models.CharField(max_length=100, blank=True)
    date_received = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    order_number = models.CharField(max_length=100, blank=True)
    qr_code = models.CharField(max_length=200, blank=True, default="")
    holder = models.CharField(max_length=100, default=None, blank=True)
    status = models.CharField(
        max_length=20, choices=[("available", "Available"), ("outinuse", "Out In Use")]
    )

    def __str__(self):
        return self.name


# Table for consumables, that are being used and never returned
class Consumable(models.Model):
    items_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    price_per_unit = models.PositiveIntegerField(default=0)
    total_quantity = models.PositiveIntegerField(default=1)
    quantity_unit  = models.CharField(max_length=20, default="PCS")
    total_price = models.PositiveIntegerField(default=0)
    min_alert_quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()
    vendor = models.CharField(max_length=100, blank=True)
    date_received = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    holder = models.CharField(max_length=100, default=None, blank=True)
    order_number = models.CharField(max_length=100, blank=True)
    qr_code = models.CharField(max_length=200, blank=True, default="")


    def __str__(self):
        return self.name


# Table for Licenses 
class License(models.Model):
    license_id = models.CharField(max_length=20)
    license_name = models.CharField(max_length=100)
    purchase_cost = models.PositiveIntegerField()
    notification_days = models.PositiveIntegerField()
    licensed_to = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    product_key = models.TextField()
    licensed_by = models.CharField(max_length=100, blank=True)
    purchased_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    order_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Table for Items that are out in use
class Loan(models.Model):
    item_title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    requestor = models.CharField(max_length=100)
    check_out_by = models.ForeignKey(User, on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.requestor}-{self.item.name}"

