from django.urls import path
from . import views

# url maps for www app
urlpatterns = [
    path('', views.homeView, name='home'),
]