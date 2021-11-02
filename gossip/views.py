from django.shortcuts import render
from .models import Neighbourhood,Business

# Create your views here.
def home(request):
    return render(request, 'home.html')
