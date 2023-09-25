from django.shortcuts import render
from .models import *

from .helper import sortTeams
def index(request):
    # Fetch teams from database and sort by point
    unorderedTeams = Team.objects.all()
    orderedTeams = []
    for team in unorderedTeams:
        # Querry the problems solved by team and calculate score
        solvedProblems = ProblemSolution.objects.filter(team=team)

        score = 0
        for solvedProblem in solvedProblems:
            score += solvedProblem.points

        # Create a dictionary representing the team
        orderedTeams.append({
            'name': team.name,
            'school': team.school,

            'score': score,
        })

    # Render the team standings
    context = { 'teams': sortTeams(orderedTeams)[::-1] }
    return render(request, 'view/index.html', context)

def refereeIndex(request):
    return render(request, 'referee/index.html')

def manageIndex(request):
    return render(request, 'manage/index.html')