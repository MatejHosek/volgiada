from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .models import *

def check_permissions(request, group):
    """Check if user is in a given group"""

    # Check if user is in the group
    if request.user.groups.filter(name=group).exists():
        return True
    return False

def index(request):
    # Check if the competition has begun
    competitionStart = Time.objects.get(name='start').time
    if competitionStart > timezone.now():
        # Display the countdown
        context = {
            'countdownEnd': competitionStart.timestamp() * 1000,
        }
        return render(request, 'judge/countdown.html', context)
    
    # Check if competition is over
    competitionEnd = Time.objects.get(name='end').time
    if competitionEnd < timezone.now():
        # Display the end message
        return HttpResponse('Soutěž skončila, děkujeme za účast.')

    # Display the score of teams
    teams = Team.objects.all()

    context = {
        'teams': sorted(teams, reverse=True),
        'isFrozen': Time.objects.get(name='freeze').time < timezone.now(),
        'countdownEnd': competitionEnd.timestamp() * 1000,
    }

    return render(request, 'judge/index.html', context)

def judge_view(request):
    # Check for user auth
    if request.user.is_anonymous:
        # Prompt the user to log in
        return HttpResponseRedirect(
            reverse('judge:login_view',
                    kwargs={'redirect_view': 'judge_view'})
        )

    if not check_permissions(request, 'competition_judge'):
        return HttpResponse('403 Forbidden', status=403)
    
    # TODO: Display assigned teams
    return HttpResponse(request.user)

def team_view(request):
    # TODO: Display problems and their scoring for a given team
    pass

def admin_view(request):
    # Check for user auth
    if request.user.is_anonymous:
        # Prompt the user to log in
        return HttpResponseRedirect(
            reverse('judge:login_view',
                    kwargs={'redirect_view': 'admin_view'})
        )

    if not check_permissions(request, 'competition_admin'):
        return HttpResponse('403 Forbidden', status=403)
    
    # TODO: Display teams, problems, judges, competition settings
    return HttpResponse('admin view')

def login_view(request, redirect_view):
    if request.method == 'POST':
        try:
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse(f'judge:{redirect_view}'))
        except:
            # TODO: Log an error
            pass

        # Login unsuccessful, render the login page again with a message
        return render(request, 'judge/login.html', context={'failed': True})
    
    # Render the page without an error message on the first load
    return render(request, 'judge/login.html', context={'failed': False})