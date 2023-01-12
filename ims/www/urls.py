from django.urls import path
from . import views

# url maps for www app
urlpatterns = [
    path('', views.homeView, name='home'),
    path('add_item/', views.add_item, name='add_item'),
    path('assets/', views.items, name='items'),
    path('accessories/', views.bulk_items, name='accessories'),
    path('item_detail/<int:pk>/', views.item_detail, name='item_detail'),
]