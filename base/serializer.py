from rest_framework import serializers
from .models import Event, EventName, EventsOrdered, LastEventDevice

class EventNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventName
        fields = ['id','name', 'order']

class EventSerializer(serializers.HyperlinkedModelSerializer):
    event_name = serializers.SlugRelatedField(
    many=False, 
    read_only=True,
    slug_field="name")
    class Meta:
        model = Event
        fields = ['id','device','event_name_id','time','event_name']

class EventsOrderedSerializer(serializers.HyperlinkedModelSerializer):
    event_name = serializers.SlugRelatedField(
    many=False, 
    read_only=True,
    slug_field="name")
    class Meta:
        model = EventsOrdered
        fields = ['device','event_name_id','event_name','tasks']

class LastEventDeviceSerializer(serializers.HyperlinkedModelSerializer):
    event_name = serializers.SlugRelatedField(
    many=False, 
    read_only=True,
    slug_field="name")
    class Meta:
        model = LastEventDevice
        fields = ['id','device','event_name_id','event_name','tasks']

