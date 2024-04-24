# Generated by Django 4.1.3 on 2024-03-24 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AttendeeApp', '0004_attendeedetailsmodel_attendee_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendeebookingsmodel',
            name='ticket_quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='attendeebookingsmodel',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]