from django.shortcuts import render
from django.views import generic
# from django.views.generic import CreateView, ListView
# from .models import Workout
# from .forms import WorkoutForm

from .forms import WorkoutTypeForm, WorkoutLinkedForm, WorkoutTypeCountForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import WorkoutLinked
from django.forms.models import model_to_dict
from .models import WorkoutType
from datetime import timedelta
from measurement.measures import Distance
from .models import WorkoutTypeCount
import m26

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
    user_workouts = WorkoutLinked.objects.filter(profile=request.user).order_by('-start_date')

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
            form = WorkoutLinkedForm(initial = model_to_dict(current_workout))
        return render(request, 'workout_app/edit_workout_linked.html', {'form': form})

    return render(request, 'workout_app/workout_linked_list.html', {'user_workouts': user_workouts})

def workoutSummary(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    context = {}
    context['wts'] = {}
    context['cts'] = {}
    user_workouts = WorkoutLinked.objects.filter(profile=request.user)
    for wt in WorkoutType.objects.all():
        woct = user_workouts.filter(workoutType=wt)
        if woct:
            dur_tot = timedelta()
            dist_tot = Distance()
            context['wts'][wt] = []
            if wt.has_duration:
                for iw in woct:
                    dur_tot += iw.duration
                context['wts'][wt].append(('Total Duration', dur_tot))
            if wt.has_distance_comp:
                for iw in woct:
                    dist_tot += iw.dist
                context['wts'][wt].append(('Total Distance', dist_tot))
            if dur_tot != 0 and dist_tot != 0:
                m26d = m26.Distance(dist_tot.mi)
                m26t = m26.ElapsedTime(str(dur_tot))
                m26s = m26.Speed(m26d, m26t)
                context['wts'][wt].append(('Pace per Mile', m26s.pace_per_mile()))
            if wt.has_first_count_component:
                fcc_tot = 0
                for iw in woct:
                    fcc_tot += iw.raw_count
                context['wts'][wt].append(('Total ' + wt.first_count_component.type_name, fcc_tot))
            if wt.has_second_count_component:
                scc_tot = 0
                for iw in woct:
                    scc_tot += iw.second_raw_count
                context['wts'][wt].append(('Total ' + wt.second_count_component.type_name, scc_tot))
    for ct in WorkoutTypeCount.objects.all():
        cc = 0
        for wt in WorkoutType.objects.all():
            if wt.has_first_count_component and (wt.first_count_component == ct):
                for iw in user_workouts.filter(workoutType=wt):
                    cc += iw.raw_count
            if wt.has_second_count_component and (wt.second_count_component == ct):
                for iw in user_workouts.filter(workoutType=wt):
                    cc += iw.second_raw_count
        if cc != 0:
            context['cts'][ct] = cc
    # print(context)
    # for v in context['wts']:
    #     for a in context['wts'][v]:
    #         print(a)
    return render(request, 'workout_app/workout_summary.html', context)

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
            return HttpResponseRedirect('/add_workout_linked/')
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
            return HttpResponseRedirect('/workout_linked_list')
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
            return HttpResponseRedirect('/add_workout_linked/')
    else:
        form = WorkoutTypeCountForm()
    return render(request, 'workout_app/add_workout_type_count.html', {'form': form})