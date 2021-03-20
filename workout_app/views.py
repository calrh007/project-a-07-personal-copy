from django.shortcuts import render
from django.views.generic import CreateView
from .models import Workout

def index(request):
    context = {}
    return render(request, 'workout_app/index.html', context)

class AddWorkoutView(CreateView):
    model = Workout
    template_name = 'add_workout.html'
    fields = '__all__'