from django.shortcuts import render
from .models import *

from .helper import orderTeams
def index(request):
    # Display team standings
    context = { 'teams': orderTeams() }
    return render(request, 'view/index.html', context)

def refereeIndex(request):
    return render(request, 'referee/index.html')

def manageIndex(request):
    return render(request, 'manage/index.html')