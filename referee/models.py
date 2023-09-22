from django.db import models
from view.models import Team

class Referee(models.Model):
    username = models.CharField(max_length=100)

    assignedTeams = models.ManyToManyField(Team)