from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

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

# Automatic creation of referee profile on user creation
@receiver(post_save, sender=User)
def create_referee_profile(sender, instance, created, **kwargs):
    if created:
        Referee.objects.create(user=instance)

# Automatic update of referee profile on user update
@receiver(post_save, sender=User)
def save_referee_profile(sender, instance, **kwargs):
    instance.profile.save()