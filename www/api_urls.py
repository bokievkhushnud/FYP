# api_urls.py

from django.urls import path
from . import api_views

urlpatterns = [
    # path('item/detail/<int:pk>/', api_views.ItemDetailView.as_view(), name='item-detail-api'),
    path('item/<int:item_id>/', api_views.item_details, name='item-details'),
    path('profile/', api_views.get_user_profile, name='get-user-profile'),
    path('items/', api_views.get_user_items, name='get-user-items'),
    path('broken/items/<int:item_id>/', api_views.set_item_status, name='set_item_status'),
    path('change_profile_pic/', api_views.change_profile_pic, name='change_profile_pic'),
    path('change_password/', api_views.change_password, name='change_password'),


]
