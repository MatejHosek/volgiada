from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    """A model representing competing teams"""

    name = models.CharField(max_length=256)
    school = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name} ({self.school})'

class Problem(models.Model):
    """A model representing competition problems"""

    name = models.CharField(max_length=256, default="")
    number = models.IntegerField()

    def __str__(self):
        return f'Problem {self.number}: {self.name}'

class Score(models.Model):
    """A model representing teams' problem solutions"""

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    points = models.IntegerField()
    time = models.DateTimeField()

class Judge(models.Model):
    """A model representing teams assigned to a judge"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Time(models.Model):
    """A model representing key competition times"""

    name = models.CharField(max_length=256)
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.name}: {self.time}'
