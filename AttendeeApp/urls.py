from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login_page'),
    path('logout', views.logout , name='logout'),
    path('edit_profile', views.edit_profile, name='edit_profile'), 
    path('pop', views.pop, name='pop'),
    path('event/<int:event_id>/', views.event_page, name='event_page'),
    path('booking/<int:event_id>/', views.booking, name='booking'),
    path('checkout/<int:event_id>/', views.checkout, name='checkout'),
    path('search', views.search, name='search'),
    path('preview/<int:event_id>/', views.preview, name='preview'),
    path('mybookings', views.mybookings, name='mybookings'),
    path('feedback/<int:booking_id>', views.feedback, name='feedback'),


]