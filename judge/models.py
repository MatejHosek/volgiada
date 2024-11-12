from django.db import models

class Team(models.Model):
    """A model representing competing teams"""

    name = models.CharField(max_length=256)
    school = models.CharField(max_length=256)

class Problem(models.Model):
    """A model representing competition problems"""

    name = models.CharField(max_length=256, default="")
    number = models.IntegerField()

class Score(models.Model):
    """A model representing teams' problem solutions"""

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    points = models.IntegerField()
