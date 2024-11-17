from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def index(request):
    # TODO: Display a competition end message after end time

    # Check if the competition has begun
    competitionStart = Time.objects.get(name='start').time
    if competitionStart > timezone.now():
        # Display the countdown
        context = {
            'countdownEnd': competitionStart.timestamp() * 1000,
        }
        return render(request, 'judge/countdown.html', context)

    # Display the score of teams
    teams = Team.objects.all()

    context = {
        'teams': sorted(teams, reverse=True),
        'isFrozen': Time.objects.get(name='freeze').time < timezone.now(),
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
