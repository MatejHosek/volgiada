from django.contrib import admin
from .models import *

admin.site.register(Team)
admin.site.register(Problem)
admin.site.register(ProblemSolution)
admin.site.register(Referee)