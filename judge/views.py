from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def index(request):
    # TODO: Sort teams by the score they achieved before freeze time
    # TODO: Display a massage that the results are frozen after freeze time
    # TODO: Display a countdown before start time
    # TODO: Display a competition end message after end time

    teams = Team.objects.all()

    context = {
        'teams': teams,
    }

    return render(request, 'judge/index.html', context)

def judge_view(request):
    # TODO: Display assigned teams
    return HttpResponse(request.user)

def team_view(request):
    # TODO: Display problems and their scoring for a given team
    pass

def admin_view(request):
    # TODO: Display teams, problems, judges, competition settings
    return HttpResponse('admin view')

def login_view(request):
    # TODO: A login page, redirects back to a page after a successful login
    pass
