from django.contrib import admin
from .models import Item, GeberatedQRCode
# Register your models here.
admin.site.register(Item)
admin.site.register(GeberatedQRCode)