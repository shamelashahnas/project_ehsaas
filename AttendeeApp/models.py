from django.db import models
from OrganiserApp.models import *


# Create your models here.


#  attendee details
class AttendeeDetailsModel(models.Model):
    attendee_id = models.AutoField(primary_key=True)
    attendee_name = models.CharField(max_length=100, blank=True)
    attendee_email = models.EmailField()
    attendee_phone = models.CharField(max_length=20,blank=True)
    attendee_username = models.CharField(max_length=50, blank=True)
    attendee_password = models.CharField(max_length=20)
    attendee_image = models.ImageField(upload_to='images/', null=True, blank=True)
    attendee_role = models.CharField(max_length=50)
    attendee_created_on = models.DateField(auto_now_add=True)
    attendee_status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.attendee_name}'

    class Meta:
        db_table = 'attendee_details'


# attendee profile images
class AttendeeImagesModel(models.Model):
    attendee_id = models.ForeignKey(AttendeeDetailsModel, on_delete=models.CASCADE)
    attendee_image_id = models.AutoField(primary_key=True)
    attendee_image = models.ImageField(upload_to='images/', null=True)

    class Meta:
        db_table = 'attendee_image_table'


# for booking events
class AttendeeBookingsModel(models.Model):
    booking_id = models.AutoField(primary_key=True)
    attendee_id = models.ForeignKey(AttendeeDetailsModel, on_delete=models.CASCADE)
    event_id = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(EventTicketModel, on_delete=models.CASCADE)
    ticket_quantity = models.IntegerField(null=True)
    total_price= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    booked_on = models.DateField(auto_created=True)

    class Meta:
        db_table = 'attendee_bookings'


# for attendee's feedback

class AttendeeFeedbackModel(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    booking_id = models.ForeignKey(AttendeeBookingsModel, on_delete=models.CASCADE)
    attendee_feedback = models.CharField(max_length=200)
    attendee_rating = models.IntegerField()

    class Meta:
        db_table = 'attendee_feedback'
