from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AdminDetailsModel)
admin.site.register(StateModel)
admin.site.register(CityModel)
admin.site.register(EventTypeModel)
admin.site.register(EventTypeImageModel)