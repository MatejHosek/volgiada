from django.contrib import admin

from .models import *

admin.site.register(Team)
admin.site.register(Problem)
admin.site.register(Score)
admin.site.register(Judge)
admin.site.register(Time)
