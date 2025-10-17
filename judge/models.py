from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from functools import *

class Time(models.Model):
    """A model representing key competition times"""

    name = models.CharField(max_length=256)
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.name}: {self.time}'

@total_ordering
class Team(models.Model):
    """A model representing competing teams"""

    name = models.CharField(max_length=256)
    school = models.CharField(max_length=256)

    def count_points(
            self,
            time = None
        ):
        """Counts the Team's points achieved before the specified time
        (defaults to min(now, competition freeze time))
        """

        # If time isn't set, set it to now or competition freeze
        if time == None:
            time = Time.objects.get(name='freeze').time

        points = 0
        for score in self.score_set.filter(time__lte=time):
            points += score.points

        return points

    def __str__(self):
        return f'{self.name} ({self.school})'
    
    # TODO: Write tests for comparator
    def __lt__(self, other: 'Team'):
        # Compare score
        if other.count_points() > self.count_points(): return True
        if other.count_points() < self.count_points(): return False
        
        # Compare highest solved problem
        time = Time.objects.get(name='freeze').time
        my_max = self.score_set.filter(time__lte=time).order_by('-problem')[0].problem.number
        ot_max = other.score_set.filter(time__lte=time).order_by('-problem')[0].problem.number

        if ot_max > my_max: return True
        if ot_max < my_max: return False

        # Compare last solved problem time
        time = Time.objects.get(name='freeze').time
        my_time = self.score_set.filter(time__lte=time).order_by('-time')[0].time
        ot_time = other.score_set.filter(time__lte=time).order_by('-time')[0].time

        if ot_time > my_time: return True
        if ot_time < my_time: return False

        # Compare alphabetically
        if other.name < self.name: return True
        if other.name > self.name: return False

class Problem(models.Model):
    """A model representing competition problems"""

    name = models.CharField(max_length=256, default="")
    number = models.IntegerField()

    def __str__(self):
        return f'{self.number}: {self.name}'

class Score(models.Model):
    """A model representing teams' problem solutions"""

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    points = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.team}-{self.problem}: {self.points} at {self.time}'

class Judge(models.Model):
    """A model representing teams assigned to a judge"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
