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



def signup(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if user_type == "organiser":
            new_organiser = OrganiserDetailsModel()
            new_organiser.organiser_email = email
            new_organiser.organiser_password = password
            new_organiser.organiser_role = user_type
            new_organiser.save()
            return redirect('/login')

        else:
            new_attendee = AttendeeDetailsModel()
            new_attendee.attendee_email = email
            new_attendee.attendee_password = password
            new_attendee.attendee_role = user_type
            new_attendee.save()
            return redirect('/login')

  

    return render(request, 'attendee/signup.html')

def edit_profile(request):
    if 'user' in request.session:
        attendee_id = request.session['user']
        user = AttendeeDetailsModel.objects.get(attendee_id=attendee_id)
    else:
        organiser_id = request.session['organiser']
        user = OrganiserDetailsModel.objects.get(organiser_id=organiser_id)

    if request.method == "POST":
        if 'user' in request.session:
            user.attendee_name = request.POST.get('name')
            user.attendee_phone = request.POST.get('phone')
            user.attendee_email = request.POST.get('email')
            user.attendee_username = request.POST.get('username')
            user.attendee_password = request.POST.get('password')
            if 'image' in request.FILES:
                image = request.FILES['image']
                user.attendee_image.save(image.name, image)
            user.save()

           

            return redirect('/')
        else:
            user.organiser_name = request.POST.get('name')
            user.organiser_phone = request.POST.get('phone')
            user.organiser_email = request.POST.get('email')
            user.organiser_username = request.POST.get('username')
            user.organiser_password = request.POST.get('password')

            if 'image' in request.FILES:
                image = request.FILES['image']
                user.organiser_image.save(image.name, image)

            user.save()

            return redirect('/')



    return render(request, 'attendee/edit_profile.html' , {'user': user})
def login(request):
    """
    Log in the attendee.
    
    This function handles the login process for attendees. It accepts POST requests with user data and password. 
    It checks if the provided credentials match any attendee in the database. If a match is found, it sets the user's 
    session and redirects to the homepage. If no match is found, it renders the login page again.
    """
    if request.method == "POST":
        user_data = request.POST.get('user_data')
        password = request.POST.get('password')
        organiser = OrganiserDetailsModel.objects.filter(
            Q(organiser_username=user_data) | Q(organiser_email=user_data) | Q(organiser_phone=user_data),
            organiser_password=password).first()
        user = AttendeeDetailsModel.objects.filter(
            Q(attendee_username=user_data) | Q(attendee_email=user_data) | Q(attendee_phone=user_data),
            attendee_password=password).first()
        
        if user:
            request.session['user'] = user.attendee_id
            return redirect('/')
        elif organiser:
            request.session['organiser'] = organiser.organiser_id
            return redirect('/')
        else:
            return render(request, 'attendee/login.html')
        
    return render(request, 'attendee/login.html')

def logout(request):
    """
    Log out the attendee.

    This function handles the logout process for attendees. It deletes the user's session and redirects to the login page.
    """
    if 'user' in request.session:
        del request.session['user']
    else:
        del request.session['organiser']
    return redirect('/')



def homepage(request):
    if 'user' in request.session:
        user_id = request.session.get('user', None)
        if user_id:
            event_type_list_key = f'event_type_list_{user_id}'
            event_type_list = request.session.get(event_type_list_key, [])
        else:
            event_type_list = []

        event_type_counts = Counter(event_type_list)

        most_visited_event_type_ids = [event_type_id for event_type_id, _ in event_type_counts.most_common(2)]  
        most_visited_event_types = EventTypeModel.objects.filter(event_type_id__in=most_visited_event_type_ids) 

        filtered_events = EventModel.objects.filter(event_type_id__in=most_visited_event_types)

    else:
        event_type_list = request.COOKIES.get('event_type_list')
        if event_type_list:
            event_type_list = json.loads(event_type_list)
        else:
            event_type_list = []    

        event_type_counts = Counter(event_type_list)

        most_visited_event_type_ids = [event_type_id for event_type_id, _ in event_type_counts.most_common(2)]  
        most_visited_event_types = EventTypeModel.objects.filter(event_type_id__in=most_visited_event_type_ids) 

        filtered_events = EventModel.objects.filter(event_type_id__in=most_visited_event_types)

    selected_location_name = None
    event_type_images = EventTypeModel.objects.prefetch_related('eventtypeimagemodel_set')
    



    filtered_events_with_images = filtered_events.prefetch_related('event_images')
    tag = EventTagsModel.objects.all()
    tags = tag.filter(Q(event_tag__icontains='Things to do in'))



    return render(request, 'attendee/homepage.html', {
        'filtered_events': filtered_events_with_images,
        'selected_location_name': selected_location_name,
        'event_type_images': event_type_images,
        'tags':tags
       
    })


   

def calculate_event_status(event):
    """
    Calculate event status.

    This function calculates the status of the event based on its start and end dates compared to the current date.
    It returns one of the following statuses: 'upcoming', 'soldout', 'expired', or 'ongoing'.
    """
    today = date.today()
    if event.booking_start_date > today:
        return 'upcoming'
    elif event.booking_end_date < today and event.event_start_date > today:
        return 'soldout'
    elif event.event_start_date < today:
        return 'expired'
    elif event.booking_start_date <= today <= event.event_start_date:
        return 'ongoing'


    

  


def event_page(request, event_id):
    """
    Render the event page.

    This function renders the event page for attendees. It retrieves event details, event images, tags, and calculates 
    the event status before rendering the template.
    """
    event = EventModel.objects.get(event_id = event_id)

    if 'user' in request.session:
        user_id = request.session['user']
        event_type_list = request.session.get(f'event_type_list_{user_id}', []) 
        event_type_list.append(event.event_type_id.event_type_id )  
        request.session[f'event_type_list_{user_id}'] = event_type_list

    event = EventModel.objects.get(event_id = event_id)
    event_image = EventImageModel.objects.get(event_id =event_id)
    tags = EventTagsModel.objects.filter(event_id = event_id)
    events_status = calculate_event_status(event)
    return render(request, 'attendee/event.html', {'event': event, 'event_status':events_status, 'event_images':event_image, 'tags':tags})


def booking(request, event_id):
    tickets = EventTicketModel.objects.filter(event_id = event_id)
    event = EventModel.objects.get(event_id = event_id)
    return render(request, 'attendee/booking.html', {'tickets':tickets, 'event':event})

def checkout(request, event_id):
    if 'user' in request.session:
        user_id = request.session['user']
        attendee= AttendeeDetailsModel.objects.get(attendee_id=user_id)
        event = EventModel.objects.get(event_id=event_id)
        ticket_type = request.GET.get('ticket_type')
        ticket = EventTicketModel.objects.get(event_id=event_id, ticket_type=ticket_type)

        ticket_price = request.GET.get('ticket_price')
        ticket_quantity = request.GET.get('ticket_quantity')

        total_price = int(ticket_price) * int(ticket_quantity) 
        total_amount = int(total_price) + 140

        if request.method == "POST":
            booking = AttendeeBookingsModel()
            booking.attendee_id = attendee
            booking.event_id = event
            booking.ticket_id = ticket
            booking.ticket_quantity = ticket_quantity
            booking.total_price = total_price
            booking.booked_on = timezone.now()
            booking.save()
            return redirect('/pop')
 
        return render(request, 'attendee/checkout.html', {
            'event': event,
            'ticket_type': ticket_type,
            'ticket_price': ticket_price,
            'ticket_quantity': ticket_quantity,
            'total_price': total_price ,
            'total_amount':total_amount 
        })
    
def pop(request):
    return render(request, 'attendee/pop.html')

def search(request):
    tags = EventTagsModel.objects.all()
    events = EventModel.objects.all()
    searched= ''
    selected_location = ''
    start_date = ''
    end_date = ''

            
    if request.method == "POST":
        searched = request.POST.get('search')
        selected_location = request.POST.get('location')
        selected_date = request.POST.get('date')
        selected_price = request.POST.get('price')
        selected_status = request.POST.get('status')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

    

        if searched:
            events = EventModel.objects.filter(
                Q(event_title__icontains=searched) | 
                Q(location__city_name__icontains=searched) | 
                Q(eventtagsmodel__event_tag__icontains=searched)
            )

            events = events.distinct()

        if start_date and end_date:
            events = events.filter(event_start_date__range=[start_date, end_date])

        if selected_location:
            events = events.filter(Q(location__city_name__icontains=selected_location))

        if selected_price == 'lowest':
            events = events.order_by('ticket_price')
        elif selected_price == 'highest':
            events = events.order_by('-ticket_price')

        if selected_date:
            events = events.filter(event_start_date=selected_date)

        if selected_status == 'upcoming':
            events = events.filter(booking_start_date__gt=date.today())
        elif selected_status == 'soldout':
            events = events.filter(booking_end_date__lt=date.today())
        elif selected_status == 'expired':
            events = events.filter(event_start_date__lt=date.today(), booking_end_date__lt=date.today())
        elif selected_status == 'ongoing':
            events = events.filter(booking_start_date__lte=date.today(), event_start_date__gte=date.today())
   
    events_status = [(event, calculate_event_status(event)) for event in events]

    search_query = request.GET.get('query', '')
    
    events = events.filter(
        Q(eventtagsmodel__event_tag__icontains=search_query) |
         Q(event_type_id__event_type__icontains=search_query) |
        Q(location__city_name__icontains=search_query) 
    ).distinct()
    

    return render(request, 'attendee/search.html', {'tags': tags, 'events_status': events_status,
                                                    
                                                    'search_query': search_query, 'events': events})




def preview(request, event_id):
    return render(request, 'attendee/preview.html',{'event_id': event_id})


def mybookings(request):
    if 'user' in request.session:
        user_id  = request.session['user']
        bookings = AttendeeBookingsModel.objects.filter(attendee_id = user_id)

        # Similarly, for future bookings based on event's start date
        future_bookings = bookings.filter(event_id__event_start_date__gte=timezone.now().date())
        past_bookings = bookings.filter(event_id__event_start_date__lt=timezone.now().date())
      
        
        return render(request, 'attendee/mybookings.html', {'bookings': bookings, 'future_bookings':future_bookings, 'past_bookings': past_bookings,})
    

    
def feedback(request, booking_id):
    booking = AttendeeBookingsModel.objects.get(pk = booking_id)

    if request.method == "POST":
        feedback = AttendeeFeedbackModel()
        feedback.booking_id = booking
        feedback.attendee_rating = request.POST.get('rating')
        feedback.attendee_feedback = request.POST.get('feedback')
        feedback.save()
        return redirect('/mybookings')

    
    return render(request, 'attendee/feedback.html', {'booking': booking})