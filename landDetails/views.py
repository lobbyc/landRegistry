from django.http import HttpResponse
from django.shortcuts import render
from . models import Landmark

# Create your views here.

lands = [
    {'id': 1, 'name': 'my land'},
    {'id':2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Nchiru lands'}
]

def home(request):
    lands=Landmark.objects.all()
    
    return render(request, 'landDetails/home.html', {'lands': lands})


def land(request):
    return render(request, "landDetails/land.html")

