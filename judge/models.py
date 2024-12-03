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
            time = min(timezone.now(), Time.objects.get(name='freeze').time)

        points = 0
        for score in self.score_set.filter(time__lte=time):
            points += score.points

        return points

    def __str__(self):
        return f'{self.name} ({self.school})'
    
    # TODO: Write tests for comparator
    def __lt__(self, other):
        # Check if both teams solved at least one problem
        # If both teams haven't solved any problems, sort alphabetically
        if len(self.score_set.all()) == 0 and len(self.score_set.all()) == 0:
            print('Sorting alphabetically')
            return self.name < other.name
        
        # If one team hasn't solved any problems, sort it lower
        if len(self.score_set.all()) == 0 or len(self.score_set.all()) == 0:
            print('One team hasn\'t solved any problems')
            return len(self.score_set.all()) < len(other.score_set.all())
        
        # Check for the number of points
        if self.count_points() < other.count_points():
            return True
        
        # Check for the highest solved problem number
        if (self.score_set.all().order_by('problem')[0].problem.number <
            other.score_set.all().order_by('problem')[0].problem.number):
            return True
        
        # Check for time of last problem submission
        return (self.score_set.all().order_by('time')[0].time >
                other.score_set.all().order_by('time')[0].time)

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
