from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(OrganiserDetailsModel)
admin.site.register(EventModel)
admin.site.register(EventImageModel)
admin.site.register(EventTagsModel)
admin.site.register(EventTicketModel)