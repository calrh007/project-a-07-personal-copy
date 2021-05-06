from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from workout_app.models import WorkoutTypeCount, WorkoutType, WorkoutLinked, Achievement, Profile, City, validate_date_not_future, validate_positive_weight, validate_positive_dist, validate_zip
from django.core.exceptions import ValidationError
import datetime
from measurement.measures import Distance, Weight
import pgeocode, math

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

def createWorkoutLinked(workout_Type, pro_file, zip_code, startdate, oneday, enddate, dur_ation, in_tensity, distt, rawcount, secondrawcount, rawset, rawrep, weightt):
    return WorkoutLinked.objects.create(workoutType = workout_Type, profile = pro_file, zipcode = zip_code, start_date = startdate, one_day = oneday, end_date = enddate,
    duration = dur_ation, intensity = in_tensity, dist = distt, raw_count = rawcount, second_raw_count = secondrawcount, raw_set = rawset, raw_rep = rawrep, weight = weightt)

class test_workoutLinked_Model(TestCase):

    def test_workoutLinked_zipcode(self):
        wt = createWorkoutType('HIIT', True, True, True, None, True, None, True, True, True, None)
        wl = createWorkoutLinked(wt, None, "22904", "2021-12-12", True, "2021-12-12", None, 'L', None, 0, 0, 1, 1, None)
        self.assertEquals(wl.zipcode, "22904")

    def test_workoutLinked_startdate(self):
        wt = createWorkoutType('HIIT', True, True, True, None, True, None, True, True, True, None)
        wl = createWorkoutLinked(wt, None, "22904", "2021-12-12", True, "2021-12-12", None, 'L', None, 0, 0, 1, 1, None)
        self.assertEquals(wl.start_date, "2021-12-12")

    def test_workoutLinked_intensity(self):
        wt = createWorkoutType('HIIT', True, True, True, None, True, None, True, True, True, None)
        wl = createWorkoutLinked(wt, None, "22904", "2021-12-12", True, "2021-12-12", None, 'L', None, 0, 0, 1, 1, None)
        self.assertEquals(wl.intensity, 'L')

    def test_workoutLinked_rawcount(self):
        wt = createWorkoutType('HIIT', True, True, True, None, True, None, True, True, True, None)
        wl = createWorkoutLinked(wt, None, "22904", "2021-12-12", True, "2021-12-12", None, 'L', None, 0, 0, 1, 1, None)
        self.assertEquals(wl.raw_count, 0)

    def test_workoutLinked_rawset(self):
        wt = createWorkoutType('HIIT', True, True, True, None, True, None, True, True, True, None)
        wl = createWorkoutLinked(wt, None, "22904", "2021-12-12", True, "2021-12-12", None, 'L', None, 0, 0, 1, 1, None)
        self.assertEquals(wl.raw_set, 1)

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

def createCity(na_me):
    return City.objects.create(name = na_me)

class test_city_model(TestCase):

    def test_achivements_title(self):
        city = createCity("Charlottesville")
        self.assertEquals(city.name, "Charlottesville")

class test_functions(TestCase):

    def test_validate_date_not_future(self):
        input_date = datetime.date(2024, 1, 2)
        with self.assertRaises(ValidationError) as context:
            validate_date_not_future(input_date)
        
        self.assertTrue('Date cannot be in the future' in str(context.exception))

    def test_validate_positive_weight(self):
        input_weight = Weight(lb = -2)
        with self.assertRaises(ValidationError) as context:
            validate_positive_weight(input_weight)
        
        self.assertTrue('Weight cannot be negative' in str(context.exception))

    def test_validate_positive_dist(self):
        input_dist = Distance(km = -40)
        with self.assertRaises(ValidationError) as context:
            validate_positive_dist(input_dist)
        
        self.assertTrue('Distance cannot be negative' in str(context.exception))

    def test_validate_zip(self):
        input_zip = "012345"
        nomi = pgeocode.Nominatim('us')
        with self.assertRaises(ValidationError) as context:
            validate_zip(input_zip)
        
        self.assertTrue(' is not a valid US zipcode' in str(context.exception))
