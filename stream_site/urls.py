
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from streamer.views import sendRTMP

def seaport(req):
	return HttpResponse("Contenido de SeaPort.cab", content_type = "application/octet-stream")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('BingBar/signed/SeaPort.cab', seaport, name='seaport_cab'),
    path('asking', sendRTMP)
]
