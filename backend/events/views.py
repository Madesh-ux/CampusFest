from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import HttpResponse
from.models import Event

def home(request):
    fest_name='CampusFest'
    registration_open = True
    events=Event.objects.all()

    return render(request,'events/home.html',{'name':fest_name,'registration_open':registration_open,'events':events})

def event_detail(request,id):
    events=get_object_or_404(Event,id=id)
    return render(request,'events/event_details.html',{'event':events})