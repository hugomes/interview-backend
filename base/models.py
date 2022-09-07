from codecs import charmap_build
from django.db import models

# Create your models here.

class EventName(models.Model):
    name = models.CharField(max_length=50, null=False)
    order = models.IntegerField(null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Event(models.Model):
    device = models.CharField(max_length=50, null=False)
    event_name = models.ForeignKey(EventName, on_delete=models.DO_NOTHING, null=False)
    time = models.IntegerField(null=False)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.device

class EventsOrdered(models.Model):
    device = models.CharField(max_length=50, null=False)
    event_name = models.ForeignKey(EventName, on_delete=models.DO_NOTHING, null=False)
    tasks = models.IntegerField()

    def __str__(self):
        return self.device

    class Meta:
        managed = False
        db_table = 'events_ordered'

class LastEventDevice(models.Model):
    device = models.CharField(max_length=50, null=False)
    tasks = models.IntegerField(default=1)
    event_name = models.ForeignKey(EventName, on_delete=models.DO_NOTHING, null=False)
    def __str__(self):
        return self.device

    class Meta:
        ordering = ['-tasks','device']

        