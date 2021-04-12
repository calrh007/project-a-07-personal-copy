from django.test import TestCase
from django.urls import reverse
from workout_app.models import WorkoutTypeCount, WorkoutType, WorkoutLinked, Achievement

def createWorkoutTypeCount(pro_file, typename):
    return WorkoutTypeCount.objects.create(profile = pro_file, type_name = typename)

class test_workoutTypeCount_model(TestCase):

    def test_workoutTypeCount_type_name(self):
        w = createWorkoutTypeCount(None, 'type name')
        self.assertEquals(w.type_name, 'type name')

def createWorkoutType(typename, intens, distancecomp, hascountcomp, firstcountcomp, hassecondcountcomp, secondcountcomp, hassetrepcomp, hasweightcomp, istype, pro_file):
    return WorkoutType.objects.create(type_name = typename, has_intensity = intens, has_distance_comp = distancecomp, has_first_count_component = hascountcomp, 
    first_count_component = firstcountcomp, has_second_count_component = hassecondcountcomp, second_count_component = secondcountcomp, has_set_rep_comp = hassetrepcomp,
    has_weight_comp = hasweightcomp, is_official_type = istype, profile = pro_file)

class test_workoutType_model(TestCase):

    def test_workoutType_type_name(self):
        wt = createWorkoutType('HIIT', True, True, True, None, True, None, True, True, True, None)
        self.assertEquals(wt.type_name, 'HIIT')

    def test_workoutType_has_intensity(self):
        wt = createWorkoutType('HIIT', True, True, True, None, True, None, True, True, True, None)
        self.assertEquals(wt.has_intensity, True)

    def test_workoutType_count_component(self):
        wt = createWorkoutType('HIIT', True, True, True, None, True, None, True, True, True, None)
        self.assertEquals(wt.first_count_component, None)

def createAchievement(ti_tle, hasspecificworkouttype, hasworkoutcountmin, hasspecificworkouttypecount, hasmintotalweight, hasminreps, hasminsingledistance, hasminsingleduration, hasmintotalduration, hasmaxpace):
    return Achievement.objects.create(title = ti_tle, has_specific_workoutType = hasspecificworkouttype, has_workout_count_min = hasworkoutcountmin, has_specific_WorkoutTypeCount = hasspecificworkouttypecount, 
    has_min_total_weight = hasmintotalweight, has_min_reps = hasminreps, has_min_single_distance = hasminsingledistance, has_min_single_duration = hasminsingleduration,
    has_min_total_duration = hasmintotalduration, has_max_pace = hasmaxpace)

class test_achievements_model(TestCase):

    def test_achivements_title(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.title, 'total_earned_points')

    def test_achivements_has_specific_workoutType(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_specific_workoutType, True)
    
    def test_achivements_has_workout_count_min(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_workout_count_min, True)

    def test_achivements_has_specific_WorkoutTypeCount(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_specific_WorkoutTypeCount, True)

    def test_achivements_has_min_total_weight(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_min_total_weight, True)

    def test_achivements_has_min_reps(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_min_reps, True)

    def test_achivements_has_min_single_distance(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_min_single_distance, True)

    def test_achivements_has_min_single_duration(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_min_single_duration, True)

    def test_achivements_has_min_total_duration(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_min_total_duration, True)

    def test_achivements_has_max_pace(self):
        wt = createAchievement('total_earned_points', True, True, True, True, True, True, True, True, True)
        self.assertEquals(wt.has_max_pace, True)