from django.shortcuts import render
from django.views import generic
# from django.views.generic import CreateView, ListView
# from .models import Workout
# from .forms import WorkoutForm

from .forms import WorkoutTypeForm, WorkoutLinkedForm, WorkoutTypeCountForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import WorkoutLinked

LE = 'Please login before viewing or submitting this'

def index(request):
    context = {}
    return render(request, 'workout_app/index.html', context)

# class AddWorkoutView(CreateView):
#     model = Workout
#     from_class = WorkoutForm
#     template_name = 'workout_app/add_workout.html'
#     fields = '__all__'

# class WorkoutListView(generic.ListView):
#     model = Workout
#     object_list = Workout.objects.all()
#     template_name = 'workout_app/workout_list.html'
#     fields = '__all__'

def workoutLinkedListView(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    user_workouts = WorkoutLinked.objects.filter(profile=request.user)

    if (request.GET.get('DeleteButton')):
        WorkoutLinked.objects.filter(id=request.GET.get('DeleteButton')).delete()
        return render(request, 'workout_app/workout_linked_list.html', {'user_workouts': user_workouts})

    if (request.GET.get('EditButton')):
        current_workout = WorkoutLinked.objects.get(id=request.GET.get('EditButton'))

        if request.method == 'POST':
            form = WorkoutLinkedForm(request.POST, instance = current_workout)
            if form.is_valid():
                ots = form.save(commit=False)
                ots.profile = request.user
                ots.save()
                return HttpResponseRedirect('/workout_linked_list/')
        else:
            form = WorkoutLinkedForm()
        return render(request, 'workout_app/edit_workout_linked.html', {'form': form})

    return render(request, 'workout_app/workout_linked_list.html', {'user_workouts': user_workouts})

def newWorkoutType(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = WorkoutTypeForm(request.POST)
        if form.is_valid():
            ots = form.save(commit=False)
            ots.profile = request.user
            ots.save()
            return HttpResponseRedirect('/')
    else:
        form = WorkoutTypeForm()
    return render(request, 'workout_app/add_workout_type.html', {'form': form})

def newWorkoutLinked(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = WorkoutLinkedForm(request.POST)
        if form.is_valid():
            ots = form.save(commit=False)
            ots.profile = request.user
            ots.save()
            return HttpResponseRedirect('/')
    else:
        form = WorkoutLinkedForm()
    return render(request, 'workout_app/add_workout_linked.html', {'form': form})

def newWorkoutTypeCount(request):
    if request.user.is_anonymous:
        messages.error(request,LE)
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = WorkoutTypeCountForm(request.POST)
        if form.is_valid():
            ots = form.save(commit=False)
            ots.profile = request.user
            ots.save()
            return HttpResponseRedirect('/')
    else:
        form = WorkoutTypeCountForm()
    return render(request, 'workout_app/add_workout_type_count.html', {'form': form})