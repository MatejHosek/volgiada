from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def index(request):
    teams = Team.objects.all() # TODO: Sort teams by their score

    context = {
        'teams': teams,
    }

    return render(request, 'judge/index.html', context)

def judge_view(request):
    return HttpResponse('judge view')

def admin_view(request):
    return HttpResponse('admin view')