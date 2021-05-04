from django.shortcuts import render
import requests
from django.views import generic
# from django.views.generic import CreateView, ListView
# from .models import Workout
# from .forms import WorkoutForm

from .forms import WorkoutTypeForm, WorkoutLinkedForm, WorkoutTypeCountForm, CityForm, UsernameChangeForm, ZipChangeForm, ModularWorkoutLinkedForm, ChooseWorkoutTypeForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import WorkoutLinked
from django.forms.models import model_to_dict
from .models import WorkoutType
from datetime import datetime, timedelta
from measurement.measures import Distance, Weight
from .models import WorkoutTypeCount
import m26

from .models import Achievement
from .models import Profile
from .models import City
from django.template.defaultfilters import pluralize

import datetime

import pgeocode

from django.contrib.auth.models import User
from django.db.models import Sum

LE = 'Please login before viewing or submitting this'

def index(request):
    context = {}
    return render(request, 'workout_app/index.html', context)

def ensure_profile(user_te):
    try:
        user_profile = user_te.profile
    except:
        new_profile = Profile(user = user_te)
        new_profile.save()

def login_view(request):
    if not request.user.is_anonymous:
        ensure_profile(request.user)
    context = {}
    return render(request, 'workout_app/login.html', context)

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

def achievementEarned(achivement, workouts):
    tf = workouts.all()
    if achivement.has_start_date:
        tf_temp = tf.filter(start_date__gte = achivement.start_date, one_day = True)
        tf = tf_temp | tf.filter(end_date__gte = achivement.start_date, one_day = False)
    if achivement.has_end_date:
        tf = tf.filter(start_date__lte = achivement.end_date)
    if achivement.has_specific_workoutType:
        if achivement.has_second_specific_workoutType:
            tf = tf.filter(workoutType__in = [achivement.specific_workoutType, achivement.second_specific_workoutType])
        else:
            tf = tf.filter(workoutType = achivement.specific_workoutType)
    if achivement.has_workout_count_min:
        if tf.count() < achivement.workout_count_min:
            return False
    if achivement.has_specific_WorkoutTypeCount:
        spec_count = 0
        for wo in tf.filter(workoutType__has_first_count_component = True, workoutType__first_count_component = achivement.specific_WorkoutTypeCount):
            spec_count += wo.raw_count
        for wo in tf.filter(workoutType__has_second_count_component = True, workoutType__second_count_component = achivement.specific_WorkoutTypeCount):
            spec_count += wo.second_raw_count
        if spec_count < achivement.specific_WorkoutTypeCount_min:
            return False
    if achivement.has_second_specific_WorkoutTypeCount:
        spec_count = 0
        for wo in tf.filter(workoutType__has_first_count_component = True, workoutType__first_count_component = achivement.second_specific_WorkoutTypeCount):
            spec_count += wo.raw_count
        for wo in tf.filter(workoutType__has_second_count_component = True, workoutType__second_count_component = achivement.second_specific_WorkoutTypeCount):
            spec_count += wo.second_raw_count
        if spec_count < achivement.second_specific_WorkoutTypeCount_min:
            return False
    if achivement.has_min_single_weight:
        satis = False
        for wo in tf.filter(workoutType__has_weight_comp = True):
            if wo.weight >= achivement.min_single_weight:
                satis = True
                break
        if not satis:
            return False
    if achivement.has_min_total_weight:
        weight_tot = Weight()
        for wo in tf.filter(workoutType__has_weight_comp = True, workoutType__has_set_rep_comp = False):
            weight_tot += wo.weight
        for wo in tf.filter(workoutType__has_weight_comp = True, workoutType__has_set_rep_comp = True):
            weight_tot += (wo.raw_set * wo.raw_rep * wo.weight)
        if weight_tot < achivement.min_total_weight:
            return False
    if achivement.has_min_reps:
        reps_tot = 0
        for wo in tf.filter(workoutType__has_set_rep_comp = True):
            reps_tot += (wo.raw_set * wo.raw_rep)
        if reps_tot < achivement.min_reps:
            return False
    if achivement.has_min_single_distance:
        satis = False
        for wo in tf.filter(workoutType__has_distance_comp = True):
            if wo.dist >= achivement.min_single_distance:
                satis = True
                break
        if not satis:
            return False
    if achivement.has_min_total_distance:
        dist_tot = Distance()
        for wo in tf.filter(workoutType__has_distance_comp = True):
            dist_tot += wo.dist
        if dist_tot < achivement.min_total_distance:
            return False
    if achivement.has_min_single_duration:
        satis = False
        for wo in tf.filter(workoutType__has_duration = True):
            if wo.duration >= achivement.min_single_duration:
                satis = True
                break
        if not satis:
            return False
    if achivement.has_min_total_duration:
        dur_tot = timedelta()
        for wo in tf.filter(workoutType__has_duration = True):
            dur_tot += wo.duration
        if dur_tot < achivement.min_total_duration:
            return False
    if achivement.has_max_pace:
        tf_temp = tf.filter(workoutType__has_distance_comp = True, workoutType__has_duration = True)
        if achivement.has_min_single_duration:
            tf_temp = tf_temp.filter(duration__gte = achivement.min_single_duration)
        if achivement.has_min_single_distance:
            tf_temp = tf_temp.filter(dist__gte = achivement.min_single_distance)
        satis = False
        for wo in tf_temp:
            m26d = m26.Distance(wo.dist.mi)
            m26t = m26.ElapsedTime(int(wo.duration.total_seconds()))
            m26s = m26.Speed(m26d, m26t)
            try:
                t = datetime.strptime(m26s.pace_per_mile(),"%M:%S.%f")
                if timedelta(hours=t.hour, minutes=t.minute, seconds=t.second) <= achivement.max_pace_per_mile:
                    satis = True
                    break
            except:
                pass # divide by zero for Pace per mile
        if not satis:
            return False
    return True

def achievementsView(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    ensure_profile(request.user)
    user_workouts = WorkoutLinked.objects.filter(profile=request.user)
    context = {}
    # context['achievements_calc'] = [(a, achievementEarned(a, user_workouts)) for a in Achievement.objects.all()]
    context['achievements_calc'] = []
    context['total_possible_points'] = 0
    context['total_earned_points'] = 0
    context['total_missed_points'] = 0
    context['total_possible_achievement_num'] = 0
    context['total_earned_achievement_num'] = 0
    context['total_missed_achievement_num'] = 0
    for a in Achievement.objects.all():
        context['total_possible_points'] += a.points
        context['total_possible_achievement_num'] += 1
        if achievementEarned(a, user_workouts):
            context['achievements_calc'].append((a, True))
            context['total_earned_points'] += a.points
            context['total_earned_achievement_num'] += 1
        else:
            context['achievements_calc'].append((a, False))
            context['total_missed_points'] += a.points
            context['total_missed_achievement_num'] += 1
    # context['point_delta'] = context['total_earned_points'] - request.user.profile.achievement_points
    point_delta = context['total_earned_points'] - request.user.profile.achievement_points
    if point_delta > 0:
        messages.info(request, ("You've gained {pi} point" + pluralize(point_delta) + " since last checking your achievements").format(pi = point_delta))
    elif point_delta < 0:
        messages.info(request, ("You've lost {pi} point" + pluralize(-1 * point_delta) + " since last checking your achievements").format(pi = -1 * point_delta))
    achievement_num_delta = context['total_earned_achievement_num'] - request.user.profile.achievement_num
    if achievement_num_delta > 0:
        messages.info(request, ("You've gained {pi} achievement" + pluralize(achievement_num_delta) + " since last checking your achievements").format(pi = achievement_num_delta))
    elif achievement_num_delta < 0:
        messages.info(request, ("You've lost {pi} achievement" + pluralize(-1 * achievement_num_delta) + " since last checking your achievements").format(pi = -1 * achievement_num_delta))
    request.user.profile.achievement_points = context['total_earned_points']
    request.user.profile.achievement_num = context['total_earned_achievement_num']
    request.user.profile.save()
    return render(request, 'workout_app/achievements.html', context)

def workoutLinkedListView(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    user_workouts = WorkoutLinked.objects.filter(profile=request.user).order_by('-start_date')

    if (request.GET.get('WeatherButton')):
        current_workout = WorkoutLinked.objects.get(id=request.GET.get('WeatherButton'))
        y = int(current_workout.get_year())
        m = int(current_workout.get_month())
        d = int(current_workout.get_day())
        start = str(int(datetime.datetime(y, m, d, 12, 0, 0).timestamp()))
        end = str(int(datetime.datetime(y, m, d, 12, 0, 0).timestamp()))

        # city = 'charlottesville'

        # url = 'http://history.openweathermap.org/data/2.5/history/city?q=' + city + ',us&type=hour&start=' + start + '&end=' + end + '&units=imperial&appid=4b11880620bbfa64946645fe86d99eb5'

        nomi = pgeocode.Nominatim('us')
        postal_query = nomi.query_postal_code(current_workout.zipcode)
        lat = str(postal_query.latitude)
        lon = str(postal_query.longitude)

        url = 'http://history.openweathermap.org/data/2.5/history/city?lat=' + lat + '&lon=' + lon + '&type=hour&start=' + start + '&end=' + end + '&units=imperial&appid=4b11880620bbfa64946645fe86d99eb5'

        city_weather = requests.get(url).json()

        weather_info = {
            'city': postal_query.place_name,
            'temperature': "{0:.2f}".format( 1.8 * (city_weather['list'][0]['main']['temp'] - 273) + 32 ),
            'description': city_weather['list'][0]['weather'][0]['description'],
            'icon': city_weather['list'][0]['weather'][0]['icon']
        }
        context = {'weather_info': weather_info, 'current_workout': current_workout}
        return render(request, 'workout_app/workout_weather.html', context)

    if (request.GET.get('DeleteButton')):
        current_workout = WorkoutLinked.objects.get(id=request.GET.get('DeleteButton'))
        if current_workout.profile != request.user:
            return HttpResponseRedirect('/')
        current_workout.delete()
        return render(request, 'workout_app/workout_linked_list.html', {'user_workouts': user_workouts})

    if (request.GET.get('EditButton')):
        current_workout = WorkoutLinked.objects.get(id=request.GET.get('EditButton'))
        if current_workout.profile != request.user:
            return HttpResponseRedirect('/')
        if request.method == 'POST':
            form = ModularWorkoutLinkedForm(request.POST, instance = current_workout, workout_type = current_workout.workoutType)
            if form.is_valid():
                ots = form.save(commit=False)
                ots.profile = request.user
                ots.save()
                return HttpResponseRedirect('/workout_linked_list/')
        else:
            form = ModularWorkoutLinkedForm(initial = model_to_dict(current_workout), workout_type = current_workout.workoutType)
        if 'weight' in form.errors:
            messages.error(request, form.errors['weight'][0])
        if 'dist' in form.errors:
            messages.error(request, form.errors['dist'][0])
        return render(request, 'workout_app/edit_workout_linked.html', {'form': form})

    return render(request, 'workout_app/workout_linked_list.html', {'user_workouts': user_workouts})

def leaderboard_context(workout_types, workouts_to_consider, workout_type_counts, num_spots):
    leader_board_context = []
    zero_dist = Distance()
    zero_dur = timedelta()
    for wt in workout_types:
        leader_board_context.append((wt, []))
        dur_list = []
        dist_list = []
        for user in User.objects.all():
            wotc = workouts_to_consider.filter(profile=user, workoutType=wt)
            if wt.has_duration:
                dur_tot = wotc.aggregate(Sum('duration'))['duration__sum']
                if dur_tot is not None and dur_tot > zero_dur:
                    dur_list.append((dur_tot, user))
            if wt.has_distance_comp:
                dist_tot = wotc.aggregate(Sum('dist'))['dist__sum']
                if dist_tot is not None and dist_tot > zero_dist:
                    dist_list.append((dist_tot, user))
        for l, t in [(dur_list, 'Total Duration'), (dist_list, 'Total Distance')]:
            if l:
                l.sort(key=lambda x:x[0], reverse=True)
                l = l[:num_spots]
                list_proc = [(1, l[0][0], l[0][1])]
                for i in range(1, len(l)):
                    if l[i][0] == l[i - 1][0]:
                        list_proc.append((list_proc[-1][0], l[i][0], l[i][1]))
                    else:
                        list_proc.append((list_proc[-1][0] + 1, l[i][0], l[i][1]))
                leader_board_context[-1][1].append((t, list_proc))
        if not leader_board_context[-1][0]:
            leader_board_context.pop()
    leader_board_context.append(('Workout Count Components', []))
    for ct in workout_type_counts:
        ct_list = []
        for user in User.objects.all():
            cc = 0
            wotc_fc = WorkoutLinked.objects.filter(profile=user, workoutType__has_first_count_component = True, workoutType__first_count_component = ct)
            wotc_fc_sum = wotc_fc.aggregate(Sum('raw_count'))['raw_count__sum']
            if wotc_fc_sum is not None:
                cc += wotc_fc_sum
            wotc_sc = WorkoutLinked.objects.filter(profile=user, workoutType__has_second_count_component = True, workoutType__second_count_component = ct)
            wotc_sc_sum = wotc_sc.aggregate(Sum('second_raw_count'))['second_raw_count__sum']
            if wotc_sc_sum is not None:
                cc += wotc_sc_sum
            if cc > 0:
                ct_list.append((cc, user))
        if ct_list:
            ct_list.sort(key=lambda x:x[0], reverse=True)
            ct_list = ct_list[:num_spots]
            ct_list_proc = [(1, ct_list[0][0], ct_list[0][1])]
            for i in range(1, len(ct_list)):
                if ct_list[i][0] == ct_list[i - 1][0]:
                    ct_list_proc.append((ct_list_proc[-1][0], ct_list[i][0], ct_list[i][1]))
                else:
                    ct_list_proc.append((ct_list_proc[-1][0] + 1, ct_list[i][0], ct_list[i][1]))
            leader_board_context[-1][1].append(('Total ' + str(ct), ct_list_proc))
    leader_board_context = [lbi for lbi in leader_board_context if lbi[1]]
    return leader_board_context

def Leaderboard(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    context = {}

    all_workouts = WorkoutLinked.objects.all()
    context['days_back_poss'] = ((0, 'All Time'), (365, 'Past Year'), (30, 'Past Month'), (7, 'Past Week'))
    try:
        days_back = int(request.GET.get('days_back', '30'))
        if days_back < 0:
            days_back = 30
    except:
        days_back = 30
    if days_back > 0:
        date_back = datetime.date.today() - datetime.timedelta(days=days_back)
        temp_filter = all_workouts.filter(start_date__gte = date_back, one_day = True)
        all_workouts = temp_filter | all_workouts.filter(end_date__gte = date_back, one_day = False)
    context['days_back'] = days_back

    context['num_spots_poss'] = (5, 10, 20, 100)
    try:
        num_spots = int(request.GET.get('num_spots', '10'))
        if num_spots <= 0:
            num_spots = 10
    except:
        num_spots = 10
    context['num_spots'] = num_spots

    only_participating_str = request.GET.get('only_participating', 'True')
    if only_participating_str == 'False':
        only_participating = False
    else:
        only_participating = True
    context['only_participating'] = only_participating

    user_workouts = all_workouts.filter(profile=request.user)
    if only_participating:
        workout_types = []
        for wt in WorkoutType.objects.all():
            if user_workouts.filter(workoutType=wt).exists():
                workout_types.append(wt)
    else:
        workout_types = WorkoutType.objects.all()

    if only_participating:
        workout_type_counts = set()
        for wt in workout_types:
            if wt.has_first_count_component:
                workout_type_counts.add(wt.first_count_component)
            if wt.has_second_count_component:
                workout_type_counts.add(wt.second_count_component)
    else:
        workout_type_counts = WorkoutTypeCount.objects.all()

    context['leader_board'] = leaderboard_context(workout_types, all_workouts, workout_type_counts, num_spots)
    return render(request, 'workout_app/leaderboard.html', context)

def workoutSummary(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')

    user_workouts = WorkoutLinked.objects.filter(profile=request.user)
    try:
        days_back = int(request.GET.get('days_back', '30'))
        if days_back < 0:
            days_back = 30
    except:
        days_back = 30
    if days_back > 0:
        date_back = datetime.date.today() - datetime.timedelta(days=days_back)
        temp_filter = user_workouts.filter(start_date__gte = date_back, one_day = True)
        user_workouts = temp_filter | user_workouts.filter(end_date__gte = date_back, one_day = False)
    context = {}

    context['days_back_poss'] = ((0, 'All Time'), (365, 'Past Year'), (30, 'Past Month'), (7, 'Past Week'))
    context['days_back'] = days_back

    context['wts'] = {}
    context['cts'] = {}
    for wt in WorkoutType.objects.all():
        woct = user_workouts.filter(workoutType=wt)
        if woct:
            dur_tot = timedelta()
            dist_tot = Distance()
            weight_tot = Weight()
            context['wts'][wt] = []
            if wt.has_duration:
                for iw in woct:
                    dur_tot += iw.duration
                context['wts'][wt].append(('Total Duration', dur_tot))
            if wt.has_distance_comp:
                for iw in woct:
                    dist_tot += iw.dist
                context['wts'][wt].append(('Total Distance', str(round((dist_tot).mi, 2)) + " mi"))
            if dur_tot != 0 and dist_tot != 0:
                m26d = m26.Distance(dist_tot.mi)
                m26t = m26.ElapsedTime(int(dur_tot.total_seconds()))
                m26s = m26.Speed(m26d, m26t)
                try:
                    context['wts'][wt].append(('Pace per Mile', m26s.pace_per_mile()))
                except:
                    pass # divide by zero for Pace per mile
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
            if wt.has_weight_comp:
                for iw in woct:
                    weight_tot += iw.weight
                context['wts'][wt].append(('Average Weight per Workout', str(round((weight_tot / len(woct)).lb, 2)) + " lb"))
            if wt.has_set_rep_comp:
                st = 0
                rt = 0
                for iw in woct:
                    st += iw.raw_set
                    rt += (iw.raw_set * iw.raw_rep)
                avg_rps = rt / st
                context['wts'][wt].append(('Total Sets', st))
                context['wts'][wt].append(('Average Reps per Set', round(avg_rps, 2)))
                context['wts'][wt].append(('Total Reps', rt))
                if weight_tot != 0:
                    weight_tot_w = Weight()
                    for iw in woct:
                        weight_tot_w += (iw.raw_set * iw.raw_rep) * iw.weight
                    try:
                        context['wts'][wt].append(('Average Weight per Rep', str(round((weight_tot_w / rt).lb, 2)) + " lb"))
                    except:
                        print("divide by zero for Average Weight per Rep")
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

def changeUsername(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.save()
            return HttpResponseRedirect('/login/')
    else:
        form = UsernameChangeForm(initial={'username': request.user.username})
    return render(request, 'workout_app/username_change.html', {'form': form})

def chooseTypeAddModularWorkout(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = ChooseWorkoutTypeForm(request.POST)
        if form.is_valid():
            workout_type = form.cleaned_data['workout_type']
            return HttpResponseRedirect('/add_workout_modular/' + '?WorkoutTypeParam=' + str(workout_type.id))
    else:
        form = ChooseWorkoutTypeForm()
    return render(request, 'workout_app/choose_workout_type.html', {'form': form})

def addModularWorkout(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    if not request.GET.get('WorkoutTypeParam'):
        return HttpResponseRedirect('/')
    workout_type_param = WorkoutType.objects.get(id=request.GET.get('WorkoutTypeParam'))
    if request.method == 'POST':
        form = ModularWorkoutLinkedForm(request.POST, workout_type = workout_type_param)
        if form.is_valid():
            ots = form.save(commit=False)
            ots.profile = request.user
            ots.workoutType = workout_type_param
            ots.save()
            return HttpResponseRedirect('/workout_linked_list')
    else:
        form = ModularWorkoutLinkedForm(workout_type = workout_type_param)
    if 'weight' in form.errors:
        messages.error(request, form.errors['weight'][0])
    if 'dist' in form.errors:
        messages.error(request, form.errors['dist'][0])
    return render(request, 'workout_app/add_workout_modular.html', {'form': form, 'workout_type_context' : workout_type_param})

def changeZipcode(request):
    if request.user.is_anonymous:
        messages.error(request, LE)
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = ZipChangeForm(request.POST)
        if form.is_valid():
            request.user.profile.zipcode = form.cleaned_data['zipcode']
            request.user.profile.save()
            return HttpResponseRedirect('/login/')
    else:
        form = ZipChangeForm(initial={'zipcode' : request.user.profile.zipcode})
    return render(request, 'workout_app/zipcode_change.html', {'form': form})

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
        form = WorkoutLinkedForm(initial={'zipcode': request.user.profile.zipcode})
    if 'weight' in form.errors:
        messages.error(request, form.errors['weight'][0])
    if 'dist' in form.errors:
        messages.error(request, form.errors['dist'][0])
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

# def weather(request):
#     # url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=4b11880620bbfa64946645fe86d99eb5'
#     # city = 'Charlottesville'
#     # city_weather = requests.get(url.format(city)).json()

#     url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=4b11880620bbfa64946645fe86d99eb5'

#     cities = City.objects.all()

#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         if form not in cities:
#             form.save()

#     form = CityForm()

#     weather_stats = []

#     for city in cities:
#         city_weather = requests.get(url.format(city)).json()

#         current_weather = {
#             'city' : city_weather['name'],
#             'temperature' : city_weather['main']['temp'],
#             'description' : city_weather['weather'][0]['description'],
#             'icon' : city_weather['weather'][0]['icon']
#         }

#         weather_stats.append(current_weather)

#     context = {'weather_stats' : weather_stats, 'form' : form}

#     return render(request, 'workout_app/weather.html', context)