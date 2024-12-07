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

def prompt_or_403(request, group, redirect):
    """Check if user has the required rights. Returns login redirect,
    HttpResponse with status 403 if not, None if yes
    """

    # Check for user auth
    if request.user.is_anonymous:
        # Prompt the user to log in
        return HttpResponseRedirect(
            reverse('judge:login_view',
                    kwargs={'redirect_view': redirect})
        )

    if not check_permissions(request, group):
        return HttpResponse('403 Forbidden', status=403)

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
    # Check for user auth and permissions
    userStatus = prompt_or_403(request, 'competition_judge', 'judge_view')
    if userStatus:
        return userStatus
    
    # List all the assigned teams
    teams = set()
    for team in Judge.objects.all().filter(user=User.objects.all()[0]):
        teams.add(team.team)

    # Generate links for all teams
    links = []
    for team in teams:
        links.append(reverse('judge:team_view', kwargs={'team_id': team.id}))

    context = {
        'teams': list(teams),
        'links': links,
    }

    return render(request, 'judge/judge.html', context=context)

def team_view(request, team_id):
    # Check for user auth and permissions
    userStatus = prompt_or_403(request, 'competition_judge', 'judge_view')
    if userStatus:
        return userStatus
    
    team = Team.objects.get(id=team_id)

    # List all the competition problems
    problems = []
    for problem in Problem.objects.all().order_by('number').values():
        # Search for a score
        solution = Score.objects.filter(team=team, problem=problem['id'])
        if len(solution) > 0:
            solution = solution[0]
        else:
            solution = None
        
        problems.append({
            'problem': problem,
            'solution': solution,
        })

    context = {
        'team': team,
        'problems': problems,
    }

    return render(request, 'judge/team.html', context)

def admin_view(request):
    # Check for user auth and permissions
    userStatus = prompt_or_403(request, 'competition_admin', 'admin_view')
    if userStatus:
        return userStatus
    
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