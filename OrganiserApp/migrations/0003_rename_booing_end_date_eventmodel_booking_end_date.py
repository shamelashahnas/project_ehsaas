# Generated by Django 4.1.3 on 2024-02-28 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrganiserApp', '0002_alter_eventmodel_event_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventmodel',
            old_name='booing_end_date',
            new_name='booking_end_date',
        ),
    ]
