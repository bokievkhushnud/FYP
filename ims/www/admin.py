from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Item)
admin.site.register(BulkItem)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Consumable)
admin.site.register(License)
admin.site.register(Loan)

