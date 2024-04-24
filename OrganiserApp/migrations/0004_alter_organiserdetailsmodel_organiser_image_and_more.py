# Generated by Django 4.1.3 on 2024-03-17 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrganiserApp', '0003_rename_booing_end_date_eventmodel_booking_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organiserdetailsmodel',
            name='organiser_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='organiserdetailsmodel',
            name='organiser_phone',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='organiserdetailsmodel',
            name='organiser_username',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
