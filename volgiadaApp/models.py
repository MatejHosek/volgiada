from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    name = models.CharField(max_length=100)
    maxPoints = models.IntegerField()

class Team(models.Model):
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)

    solvedProblems = models.ManyToManyField(Problem, through="ProblemSolution")

class ProblemSolution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    points = models.IntegerField()
    timeSolved = models.DateTimeField()

# Referee extension of user profile
class Referee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    assignedTeams = models.ManyToManyField(Team)