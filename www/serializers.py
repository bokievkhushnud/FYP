
from rest_framework import serializers
from .models import Item, Profile, Department, Category
from .models import Profile, ItemAssignment
from django.contrib.auth.models import User
from django.db import models



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username']

    def to_representation(self, instance):
        """
        Overriding this method to handle ManyRelatedManager instances properly.
        """
        if isinstance(instance, models.Manager):
            return [super().to_representation(user) for user in instance.all()]
        return super().to_representation(instance)



class DepartmentSerializer(serializers.ModelSerializer):
    head = UserSerializer()

    class Meta:
        model = Department
        fields = ['id', 'name', 'head']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    department = DepartmentSerializer()
    holder = UserSerializer(many=True)
    class Meta:
        model = Item
        fields = ['id', 'item_name', 'item_code','item_type', 'image', 'quantity', 'price','currency', 'description', 'vendor', 'date_received', 'expiration_date', 'notes', 'order_number', 'status', 'category', 'department', 'location', 'campus', 'holder', 'qr_code', 'min_alert_quantity']



class ProfileSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = Profile
        fields = ['owner', 'profile_pic']

class ItemAssignmentSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)
    requestor = UserSerializer()
    done_by = UserSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = ItemAssignment
        fields = ['item', 'quantity', 'action', 'department', 'location', 'requestor', 'done_by', 'date', 'due_date', 'notes', 'status']
