from django.contrib import admin

# Register your models here.
from .models import LastEventDevice, Event, EventName

admin.site.register(LastEventDevice)
admin.site.register(EventName)
admin.site.register(Event)
