# Generated by Django 4.1.3 on 2024-02-23 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AdminApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventModel',
            fields=[
                ('event_created_on', models.DateField(auto_created=True)),
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_title', models.CharField(max_length=50)),
                ('event_description', models.CharField(max_length=2000)),
                ('venue', models.CharField(max_length=150, null=True)),
                ('event_start_time', models.TimeField(null=True)),
                ('event_end_time', models.TimeField(blank=True, null=True)),
                ('event_start_date', models.DateField(null=True)),
                ('event_end_date', models.DateField(blank=True, null=True)),
                ('ticket_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('free_ticket_available', models.BooleanField(default=False, null=True)),
                ('booking_start_date', models.DateField(blank=True)),
                ('booing_end_date', models.DateField(blank=True)),
                ('event_license', models.CharField(max_length=100)),
                ('event_status', models.BooleanField(default=False)),
                ('event_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.eventtypemodel')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.citymodel')),
            ],
            options={
                'db_table': 'event_table',
            },
        ),
        migrations.CreateModel(
            name='OrganiserDetailsModel',
            fields=[
                ('organiser_created_on', models.DateField(auto_created=True)),
                ('organiser_id', models.AutoField(primary_key=True, serialize=False)),
                ('organiser_name', models.CharField(max_length=100)),
                ('organiser_email', models.EmailField(max_length=254)),
                ('organiser_phone', models.CharField(max_length=50)),
                ('organiser_username', models.CharField(max_length=50)),
                ('organiser_password', models.CharField(max_length=20)),
                ('organiser_image', models.ImageField(null=True, upload_to='images/')),
                ('organiser_role', models.CharField(max_length=50)),
                ('organiser_status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'organiser_details',
            },
        ),
        migrations.CreateModel(
            name='EventTicketModel',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('ticket_type', models.CharField(max_length=20)),
                ('ticket_details', models.CharField(max_length=150)),
                ('ticket_price', models.IntegerField()),
                ('total_seats', models.IntegerField()),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrganiserApp.eventmodel')),
            ],
            options={
                'db_table': 'event_ticket_table',
            },
        ),
        migrations.CreateModel(
            name='EventTagsModel',
            fields=[
                ('event_tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_tag', models.CharField(max_length=100)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrganiserApp.eventmodel')),
            ],
            options={
                'db_table': 'event_tag_table',
            },
        ),
        migrations.AddField(
            model_name='eventmodel',
            name='organiser_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrganiserApp.organiserdetailsmodel'),
        ),
        migrations.CreateModel(
            name='EventImageModel',
            fields=[
                ('event_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_image', models.ImageField(null=True, upload_to='images/')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_images', to='OrganiserApp.eventmodel')),
            ],
            options={
                'db_table': 'event_image_table',
            },
        ),
    ]