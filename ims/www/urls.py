from django.urls import path
from . import views

# url maps for www app
urlpatterns = [
    path('', views.homeView, name='home'),
    path('add_item/', views.add_item, name='add_item'),
]