
from rest_framework import serializers
from .models import Item, Profile
from .models import Profile, ItemAssignment
from django.contrib.auth.models import User

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_name', 'image', 'quantity', 'price','currency', 'description', 'vendor', 'date_received', 'expiration_date', 'notes', 'order_number', 'status']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class ProfileSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Profile
        fields = ['owner', 'profile_pic']

class ItemAssignmentSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    requestor = UserSerializer()
    done_by = UserSerializer()

    class Meta:
        model = ItemAssignment
        fields = ['item', 'quantity', 'action', 'department', 'location', 'requestor', 'done_by', 'date', 'due_date', 'notes', 'status']
