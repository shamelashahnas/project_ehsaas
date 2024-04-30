from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from OrganiserApp.models import *
from AdminApp.models import *
from AttendeeApp.models import *
from datetime import date
from collections import Counter
import json
from datetime import datetime
from django.utils import timezone




# Create your views here.
def create_event(request):
    return render(request, 'attendee/create_event.html')

def create(request):
    if 'organiser' in request.session:
        event_types = EventTypeModel.objects.all()
        location = CityModel.objects.all()
        organiser_id = request.session['organiser']
        if request.method == "POST":
            event_title = request.POST.get('event_title')
            event_type_id = request.POST.get('event_type') 
            event_description = request.POST.get('event_description')
            event_location_id = request.POST.get('event_location')  
            event_venue = request.POST.get('event_venue')
            event_start_date = request.POST.get('event_start_date')
            event_end_date = request.POST.get('event_end_date')
            event_start_time = request.POST.get('event_start_time')
            event_end_time = request.POST.get('event_end_time')
            booking_start_date = request.POST.get('booking_start_date')
            booking_end_date = request.POST.get('booking_end_date')
            event_license = request.POST.get('event_license')

            entry_type = request.POST.get('entry_type')

            new_event = EventModel()

            new_event.event_title = event_title
            new_event.event_description = event_description
            new_event.venue = event_venue
            new_event.event_start_date = event_start_date
            new_event.event_end_date = event_end_date
            new_event.event_start_time = event_start_time
            new_event.event_end_time = event_end_time
            new_event.booking_start_date = booking_start_date
            new_event.booking_end_date = booking_end_date
            new_event.event_license = event_license

            new_event.organiser_id = OrganiserDetailsModel.objects.get(pk=organiser_id)
            new_event.event_type_id = EventTypeModel.objects.get(pk=event_type_id)
            new_event.location = CityModel.objects.get(pk=event_location_id)  
            new_event.event_created_on = datetime.now().date()

            new_event.save()
            event_id = new_event.event_id

            tags = request.POST.getlist('text[]')
            for tag in tags:
                event_tag = EventTagsModel(event_id=new_event, event_tag=tag)
                event_tag.save()

            if 'upload' in request.FILES:
                images = request.FILES.getlist('upload')                
                for image in images:
                    event_image = EventImageModel(event_id=new_event, event_image=image)
                    event_image.save()

            if entry_type == 'free':
                return redirect('preview', event_id=event_id)
            else:
                return redirect('ticket', event_id=event_id)
   
            

        return render(request, 'attendee/create.html', {'event_types': event_types, 'location': location})
    else:
        return redirect('/login/')



def ticket(request, event_id):

    if request.method == 'POST':
        ticket_type = request.POST.get('ticket_type')
        ticket_details = request.POST.get('ticket_details')
        ticket_price = request.POST.get('ticket_price')
        total_seats = request.POST.get('total_seats')
      
        

        new_ticket = EventTicketModel()

        new_ticket.ticket_type = ticket_type
        new_ticket.ticket_details = ticket_details
        new_ticket.ticket_price = ticket_price
        new_ticket.total_seats = total_seats

        event = EventModel.objects.get(pk=event_id)

        new_ticket.event_id = event
        new_ticket.save()

        ticket = EventTicketModel.objects.filter(event_id =event_id)
        least_price_ticket = EventTicketModel.objects.filter(event_id=event_id).order_by('ticket_price').first()
        event.ticket_price = least_price_ticket.ticket_price
        event.save()

       
    return render(request, 'attendee/ticket.html', {'event_id': event_id})



def your_events(request):
    if 'organiser' in request.session:
        organiser_id = request.session['organiser']

        events = EventModel.objects.filter(organiser_id=organiser_id)
    return render(request, 'attendee/your_events.html', {'events': events, })


def your_tickets(request, event_id):
    event = EventModel.objects.get(event_id=event_id)
    tickets = EventTicketModel.objects.filter(event_id=event_id)
    
    return render(request, 'attendee/your_tickets.html', {'tickets': tickets, 'event':event })
    
def edit_ticket(request, ticket_id):
    ticket = EventTicketModel.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        ticket.ticket_type = request.POST.get('ticket_type')
        ticket.ticket_details = request.POST.get('ticket_details')
        ticket.ticket_price = request.POST.get('ticket_price')
        ticket.total_seats = request.POST.get('total_seats')
        ticket.save()
        return redirect(reverse('your_tickets', kwargs={'event_id': ticket.event_id.event_id}))
   
    return render(request, 'attendee/edit_ticket.html', {'ticket': ticket})


def delete_ticket(request, ticket_id):
    ticket = EventTicketModel.objects.get(ticket_id=ticket_id)
    ticket.delete()
    return redirect(reverse('your_tickets', kwargs={'event_id': ticket.event_id.event_id}))
def edit_event(request, event_id):
    event = EventModel.objects.get(event_id=event_id)
    event_tags = EventTagsModel.objects.filter(event_id = event_id)
    images = EventImageModel.objects.filter(event_id = event_id)
    event_types = EventTypeModel.objects.all()
    location = CityModel.objects.all()

    event_start_date_formatted = event.event_start_date.strftime('%Y-%m-%d') if event.event_start_date else ''
    event_end_date_formatted = event.event_end_date.strftime('%Y-%m-%d') if event.event_end_date else ''
    event_start_time_formatted = event.event_start_time.strftime('%H:%M') if event.event_start_time else ''
    event_end_time_formatted = event.event_end_time.strftime('%H:%M') if event.event_end_time else ''
    booking_start_date_formatted = event.booking_start_date.strftime('%Y-%m-%d') if event.booking_start_date else ''
    booking_end_date_formatted = event.booking_end_date.strftime('%Y-%m-%d') if event.booking_end_date else ''


    if request.method == 'POST':
        event.event_title = request.POST.get('event_title')
        event_type_id = request.POST.get('event_type')
        if event_type_id:
            event_type_instance =EventTypeModel.objects.get(pk=event_type_id)
            event.event_type_id = event_type_instance
        event.event_description = request.POST.get('event_description')
        event.event_license = request.POST.get('event_license')
        location= request.POST.get('event_location')
        if location:
            location_instance = CityModel.objects.get(pk=location)
            event.location = location_instance
        event.venue = request.POST.get('event_venue')
        event.event_start_date = request.POST.get('event_start_date')
        event.event_end_date = request.POST.get('event_end_date')
        event.event_start_time = request.POST.get('event_start_time')
        event.event_end_time = request.POST.get('event_end_time')
        event.booking_start_date = request.POST.get('booking_start_date')
        event.booking_end_date = request.POST.get('booking_end_date')

        event.save()

        updated_tags = request.POST.getlist('tags[]')
        existing_tags = list(event_tags.values_list('event_tag', flat=True))

        for tag in updated_tags:
            if tag not in existing_tags:
                event_tag = EventTagsModel(event_id=event, event_tag=tag)
                event_tag.save()

        for tag_obj in event_tags:
            if tag_obj.event_tag not in updated_tags:
                tag_obj.delete()
        if 'upload' in request.FILES:
            new_images = request.FILES.getlist('upload')
            for image in new_images:
                event_image = EventImageModel(event_id=event, event_image=image)
                event_image.save()

        
        deleted_image_ids = [image_id for image_id in request.POST.getlist('deleted_images[]') if image_id.isdigit()]
        if deleted_image_ids:
                EventImageModel.objects.filter(event_image_id__in=deleted_image_ids).delete()


     
        return redirect('/your_events')

 

    return render(request, 'attendee/edit_event.html' , {'event': event, 
        'event_types': event_types,
        'location': location,
        'tags':event_tags,
        'images':images,
        'event_start_date_formatted': event_start_date_formatted,
        'event_end_date_formatted': event_end_date_formatted,
        'event_start_time_formatted': event_start_time_formatted,
        'event_end_time_formatted': event_end_time_formatted,
        'booking_start_date_formatted': booking_start_date_formatted,
        'booking_end_date_formatted': booking_end_date_formatted,})

