from django.urls import include, path
from rest_framework import routers
from base import views

router = routers.DefaultRouter()
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),

    path('api/eventnames', views.listAllEventNames),
    path('api/saveeventname', views.saveEventName),
    path('api/eventname/<int:pk>', views.eventName),

    path('api/events', views.events),
    path('api/lasteventdevice', views.lastEventDevice),
    path('api/eventsordered', views.eventsOrdered),
    path('api/saveevent', views.saveEvent)
]
