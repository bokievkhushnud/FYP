from django.forms import ModelForm
from .models import Item


# Form for adding new Item
class AddItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'