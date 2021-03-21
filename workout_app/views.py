from django.shortcuts import render
from django.views.generic import CreateView
from .models import Workout
from .forms import WorkoutForm

def index(request):
    context = {}
    return render(request, 'workout_app/index.html', context)

class AddWorkoutView(CreateView):
    model = Workout
    from_class = WorkoutForm
    template_name = 'workout_app/add_workout.html'
    fields = '__all__'

class WorkoutListView(CreateView):
    model = Workout
    template_name = 'workout_app/workout_list.html'
    fields = '__all__'