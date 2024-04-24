from django.urls import path
from . import views


urlpatterns =[
    path('', views.home_admin_view, name='home_admin_view'),
   
]