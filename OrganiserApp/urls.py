from django.urls import path
from . import views


urlpatterns =[
    path('create_event', views.create_event, name='create_event'),
    path('create' , views.create, name='create'),
    path('ticket/<int:event_id>', views.ticket, name='ticket'),
    path('your_events', views.your_events, name='your_events'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('your_tickets/<int:event_id>/', views.your_tickets, name='your_tickets'),
    path('edit_ticket/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
]