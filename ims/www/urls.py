from django.urls import path
from . import views

# url maps for www app
urlpatterns = [
    path('', views.homeView, name='home'),

    # Assets url
    path('items/', views.items, name='items'),
    path('item/detail/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/add/', views.add_item, name='add_item'),
    path('update/<int:pk>/', views.update, name='update_items'),
    path('update_consumabe/<int:pk>/', views.update_consumables, name='update_consumable'),



    path('accessories/add', views.add_accessory, name='add_accessories'),
    path('consumables/add', views.add_consumable, name='add_consumables'),
    path('checkout/<int:pk>', views.checkout_items, name='checkout_items'),
    path('checkin/<int:pk>', views.checkin_items, name='checkin_items'),


    # Licenses
    path('licenses/', views.licenses, name='licenses'),
    path('licenses/detail/<int:pk>/', views.licenses_detail, name='licenses_detail'),
    path('licenses/add', views.add_licenses, name='add_licenses'),

    # Bulk delete
    path('delete', views.delete_items, name="bulk_delete"),
    path('delete/<int:pk>/', views.delete_items, name="bulk_delete"),

    path('checkout', views.checkout_items, name="checkout_items"),


    # Registration
    path('register', views.register, name='register'),

]