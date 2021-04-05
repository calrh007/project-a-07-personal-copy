from django.test import TestCase
from django.urls import reverse
from workout_app.models import WorkoutTypeCount, WorkoutType, WorkoutLinked

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