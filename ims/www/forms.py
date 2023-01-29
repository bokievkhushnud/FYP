from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


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
        model = Item
        exclude = ["qr_code", "holder", "status"]

    def __init__(self, *args, **kwargs):
        super(AddBulkItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# Form for adding consumables
class AddConsumableForm(ModelForm):
    class Meta:
        model = Item
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


# Registration form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')
        model = get_user_model()

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = "Confirm Password"
        self.fields['password1'].label = "Password"
