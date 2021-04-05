from django.contrib import admin
# from .models import Workout

from .models import WorkoutType, WorkoutLinked, WorkoutTypeCount

# Register your models here.

# admin.site.register(Workout)
admin.site.register(WorkoutType)
admin.site.register(WorkoutLinked)
admin.site.register(WorkoutTypeCount)