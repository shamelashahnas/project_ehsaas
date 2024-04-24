from django.db import models


# Create your models here.
# admin details
class AdminDetailsModel(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_username = models.CharField(max_length=20)
    admin_password = models.CharField(max_length=20)
    admin_phone = models.CharField(max_length=20)
    admin_email = models.EmailField()

    class Meta:
        db_table = 'admin_details'


# for state(location)
class StateModel(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.state_name}'



    class Meta:
        db_table = 'table_state'


# for city(location)
class CityModel(models.Model):
    city_id = models.AutoField(primary_key=True)
    state_id = models.ForeignKey(StateModel, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.city_name}'



    class Meta:
        db_table = 'table_city'


# for event types
class EventTypeModel(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    event_type = models.CharField(max_length=20)

    def __str__(self):
        return self.event_type

    class Meta:
        db_table = 'event_type_table'


class EventTypeImageModel(models.Model):
    event_type_id = models.ForeignKey(EventTypeModel, on_delete=models.CASCADE)
    event_type_image_id = models.AutoField(primary_key=True)
    event_type_image = models.ImageField(upload_to='images/', null=True)


    class Meta:
        db_table = 'event_type_image_table'
