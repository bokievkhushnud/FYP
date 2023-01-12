from django.forms import ModelForm
from .models import *


# Form for adding new Item
class AddItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ["qr_code", "holder", "status"]
    
    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# Form for adding items in bulk
class AddBulkItemForm(ModelForm):
    class Meta:
        model = BulkItem
        exclude = ["qr_code", "holder", "status"]
    
    def __init__(self, *args, **kwargs):
        super(AddBulkItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# Form for adding consumables
class AddConsumableForm(ModelForm):
    class Meta:
        model = Consumable
        exclude = ["qr_code", "holder"]
    
    def __init__(self, *args, **kwargs):
        super(AddConsumableForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# Form for adding consumables
class AddLicenseForm(ModelForm):
    class Meta:
        model = License
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(AddLicenseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'