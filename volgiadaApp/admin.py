from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Display referee information inline with users
class RefereeInLine(admin.StackedInline):
    model = Referee
    can_delete = False
    verbose_name_plural = 'referees'

class UserAdmin(BaseUserAdmin):
    inlines = [RefereeInLine]

admin.site.register(Team)
admin.site.register(Problem)
admin.site.register(ProblemSolution)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)