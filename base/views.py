from .models import EventName, LastEventDevice, Event, EventsOrdered
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse 
from rest_framework import status
from django.db.models import Q

# from .models import MyData
from .serializer import EventSerializer, EventNameSerializer, LastEventDeviceSerializer, EventsOrderedSerializer

@api_view(['GET'])
def listAllEventNames(request):
    if request.method == 'GET':
        event_names = EventName.objects.all()
        serializer = EventNameSerializer(event_names, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def saveEventName(request):   
    request_data = JSONParser().parse(request)
    serializer = EventNameSerializer(data=request_data)
    if serializer.is_valid():
        allEventNames = EventName.objects.all()
        eventnames = allEventNames.filter(name__icontains=serializer.validated_data['name'])
        if not eventnames:
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def eventName(request,pk):
    if request.method == 'GET':
        event_names = EventName.objects.get(id=pk)
        serializer = EventNameSerializer(event_names, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        event_name = EventName.objects.get(pk=pk)
        if event_name:
            json_obj = JSONParser().parse(request) 
            serializer = EventNameSerializer(event_name, data=json_obj) 
            if serializer.is_valid(): 
                serializer.save() 
                return JsonResponse(serializer.data, status=status.HTTP_200_OK) 
    elif request.method == 'DELETE':
        eventname = EventName.objects.get(id=pk)
        if eventname:
            eventname.delete()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    return JsonResponse(serializer.errors, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def events(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def eventsOrdered(request):
    if request.method == 'GET':
        events = EventsOrdered.objects.all()
        serializer = EventsOrderedSerializer(events, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def lastEventDevice(request):
    if request.method == 'GET':
        events = LastEventDevice.objects.all()
        serializer = LastEventDeviceSerializer(events, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def saveEvent(request):
    request_data = JSONParser().parse(request)
    
    if not request_data['device']:
        return JsonResponse(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    serializer = EventSerializer(data=request_data)
    if serializer.is_valid():
        update = True
        actualEvent = request_data['event_name_id']

        lastEventDevice = LastEventDevice.objects.filter(device=request_data['device'])

        lastEvent = 0
        if (lastEventDevice):
            lastEvent = lastEventDevice.get().event_name_id
        update = validateUpdate(lastEvent, actualEvent)
        
        print(update)
        if update:
            Event.objects.create(
                    device = request_data['device'],
                    time = request_data['time'],
                    event_name = EventName.objects.get(id=actualEvent))
            
            countDelete = 0
            # delete touched if start call
            if actualEvent == '6':
                obj = Event.objects.filter(Q(event_name_id=2) & Q(device=request_data['device']))
                countDelete = obj.count()
                obj.delete()
            if (lastEventDevice):
                    LastEventDevice.objects.filter(id=lastEventDevice.get().id).update(
                        event_name = EventName.objects.get(id=actualEvent), 
                        tasks=lastEventDevice.get().tasks-countDelete+1)
            else:
                LastEventDevice.objects.create(
                    device = request_data['device'],
                    event_name = EventName.objects.get(id=actualEvent)
                )

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def validateUpdate(lastEvent, actualEvent):
    print(lastEvent,actualEvent)
    #save if event touch and state touch, stop and offline
    if int(lastEvent) in (4,6) and int(actualEvent) == 2:
        return False
    #save if last state offline and actual state is online 
    elif int(lastEvent) == 5 and int(actualEvent) != 4:
        return False
    elif int(lastEvent) == 0 and int(actualEvent) != 4:
        return False
    return True




    