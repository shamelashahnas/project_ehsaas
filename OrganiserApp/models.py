from django.db import models
from AdminApp.models import CityModel, EventTypeModel


# Create your models here.

# organiser details
class OrganiserDetailsModel(models.Model):
    organiser_id = models.AutoField(primary_key=True)
    organiser_name = models.CharField(max_length=100, blank=True)
    organiser_email = models.EmailField()
    organiser_phone = models.CharField(max_length=50, blank=True)
    organiser_username = models.CharField(max_length=50, blank=True)
    organiser_password = models.CharField(max_length=20)
    organiser_image = models.ImageField(upload_to='images/', null=True, blank=True)
    organiser_role = models.CharField(max_length=50)
    organiser_created_on = models.DateField(auto_now_add=True)
    organiser_status = models.BooleanField(default=True)



    def __str__(self):
        return f'{self.organiser_name}'

    class Meta:
        db_table = 'organiser_details'


# for event details
class EventModel(models.Model):
    event_id = models.AutoField(primary_key=True)
    organiser_id = models.ForeignKey(OrganiserDetailsModel, on_delete=models.CASCADE)
    event_type_id = models.ForeignKey(EventTypeModel, on_delete=models.CASCADE)
    event_title = models.CharField(max_length=50)
    event_description = models.TextField()
    location = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    venue = models.CharField(max_length=150, null=True)
    event_start_time = models.TimeField(null=True)
    event_end_time = models.TimeField(null=True, blank=True)
    event_start_date = models.DateField(null=True)
    event_end_date = models.DateField(null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    free_ticket_available = models.BooleanField(default=False,null=True)
    booking_start_date = models.DateField(blank=True)
    booking_end_date = models.DateField(blank=True)
    event_license = models.CharField(max_length=100)
    event_created_on = models.DateField(auto_created=True)
    event_status = models.BooleanField(default=False)



    def __str__(self):
        return f'{self.event_title}'


    class Meta:
        db_table = 'event_table'


# for event images
class EventImageModel(models.Model):
    event_image_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(EventModel, on_delete=models.CASCADE,related_name='event_images')
    event_image = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return f'{self.event_id.event_title}'

    class Meta:
        db_table = 'event_image_table'


# for event tags
class EventTagsModel(models.Model):
    event_tag_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    event_tag = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.event_tag}'

    class Meta:
        db_table = 'event_tag_table'


# for event tickets
class EventTicketModel(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=20)
    ticket_details = models.CharField(max_length=150)
    ticket_price = models.IntegerField()
    total_seats = models.IntegerField()

    
    def __str__(self):
        return f'{self.event_id.event_title}'

    class Meta:
        db_table = 'event_ticket_table'

    