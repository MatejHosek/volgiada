from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.decorators.clickjacking import xframe_options_sameorigin

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
    # Check for competition phase
    phase, countdown, message = None, None, None

    competitionStart = Time.objects.get(name='start').time
    if competitionStart > timezone.now():
        phase = 'start'
        countdown = competitionStart
        message = 'Soutěž brzy začne'

    competitionFreeze = Time.objects.get(name='freeze').time
    competitionEnd = Time.objects.get(name='end').time

    if phase is None:
        phase = 'ongoing'
        countdown = competitionEnd

    if competitionFreeze < timezone.now():
        phase = 'freeze'
        message = 'Konec soutěže se blíží! Výsledky byly zamrazeny'

    if competitionEnd < timezone.now():
        phase = 'end'

    context = {
        'message': message,
    }

    if phase == 'end':
        return render(request, 'judge/over.html', context)
    
    return render(request, 'judge/index.html', context)

@xframe_options_sameorigin
def leaderboard(request):
    # Load teams and their scores
    teams = []
    for team in sorted(Team.objects.all(), reverse=True):
        # Load team's solved problems
        problems = []
        for problem in Problem.objects.all().order_by('number').values():
            # Check if problem was solved after competition freeze
            freeze_time = Time.objects.get(name="freeze")

            problems.append({
                'problem': problem,
                'solved': len(Score.objects.filter(
                    team=team.id,
                    problem=problem['id'],
                    time__lte=freeze_time.time)) > 0,
            })

        teams.append({
            'team': team,
            'problems': problems,
        })

    context = {
        'teams': teams,
        'countdownEnd': Time.objects.get(name='end').time.timestamp() * 1000,
    }

    return render(request, 'judge/leaderboard.html', context)

def judge_view(request):
    # Check for user auth and permissions
    userStatus = prompt_or_403(request, 'competition_judge', 'judge_view')
    if userStatus:
        return userStatus
    
    # List all the assigned teams
    teams = set()
    for team in Judge.objects.all().filter(user=request.user):
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

        link = reverse('judge:problem_view', kwargs={
            'team_id': team.id,
            'problem_id': problem['id'],
        })
        
        problems.append({
            'problem': problem,
            'solution': solution,
            'link': link
        })

    context = {
        'team': team,
        'problems': problems,
    }

    return render(request, 'judge/team.html', context)

def problem_view(request, team_id, problem_id):
    # Display the scoring options for a given problem
    if request.method == 'GET':
        score = None
        solution = Score.objects.filter(team=team_id, problem=problem_id)
        if len(solution) > 0:
            score = solution[0].points

        context = {
            'team': Team.objects.get(id=team_id),
            'problem': Problem.objects.get(id=problem_id),
            'score': score,
            'options': range(1, 6),
        }

        return render(request, 'judge/problem.html', context)
    
    # Process the score update
    if request.method == 'POST':
        try:
            points = request.POST['points']

            # Check if score is none
            if points == 'none':
                # Delete the scoring, do not assign a new scoring
                for scoring in Score.objects.filter(team=team_id, problem=problem_id):
                    scoring.delete()
            else:
                points = int(points)
                # Check if score is within bounds
                if points < 0 or points > 6:
                    # TODO: Log an error
                    raise ValueError
                
                # Delete all existing scores
                for scoring in Score.objects.filter(team=team_id, problem=problem_id):
                    scoring.delete()

                # Add new score
                Score.objects.create(
                    team=Team.objects.get(id=team_id),
                    problem=Problem.objects.get(id=problem_id),
                    time=timezone.now(),
                    points=points,
                )
        finally:
            return HttpResponseRedirect(reverse('judge:team_view', kwargs={'team_id': team_id}))

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