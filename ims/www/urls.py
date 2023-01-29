from django.urls import path
from . import views

# url maps for www app
urlpatterns = [
    path('', views.homeView, name='home'),

    # Assets url
    path('items/', views.items, name='items'),
    path('item/detail/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/add', views.add_item, name='add_item'),

    # # Accessories
    # path('accessories/', views.bulk_items, name='accessories'),
    # path('accessories/detail/<int:pk>/', views.buik_item_detail, name='bulkitem_detail'),
    # path('accessories/add', views.add_bulkitem, name='add_accessories'),

    # # Consumables
    # path('consumables/', views.consumables, name='consumables'),
    # path('consumables/detail/<int:pk>/', views.consumables_detail, name='consumables_detail'),
    # path('consumables/add', views.add_consumables, name='add_consumables'),

    # Licenses
    path('licenses/', views.licenses, name='licenses'),
    path('licenses/detail/<int:pk>/', views.licenses_detail, name='licenses_detail'),
    path('licenses/add', views.add_licenses, name='add_licenses'),

    # Bulk delete
    path('delete', views.delete_items, name="bulk_delete"),
    path('checkout', views.checkout_items, name="bulk_checkout"),


    # Registration
    path('register', views.register, name='register'),

]