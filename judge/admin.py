from django.contrib import admin

from .models import *

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school', 'count_points']

class ProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'number']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'problem', 'points', 'time']

class JudgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'team']

class TimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'time']

admin.site.register(Team, TeamAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Judge, JudgeAdmin)
admin.site.register(Time, TimeAdmin)
