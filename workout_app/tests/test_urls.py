from django.test import SimpleTestCase
from django.urls import reverse, resolve
from workout_app.views import index, workoutLinkedListView, newWorkoutType, newWorkoutLinked, newWorkoutTypeCount, achievementsView, workoutSummary, Leaderboard, changeUsername
from workout_app.views import changeZipcode, addModularWorkout, chooseTypeAddModularWorkout


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_add_workout_type_url_resolves(self):
        url = reverse('add_workout_type')
        self.assertEquals(resolve(url).func, newWorkoutType)

    def test_add_workout_linked_resolves(self):
        url = reverse('add_workout_linked')
        self.assertEquals(resolve(url).func, newWorkoutLinked)

    def test_add_workout_type_count_resolves(self):
        url = reverse('add_workout_type_count')
        self.assertEquals(resolve(url).func, newWorkoutTypeCount)

    def test_add_workout_type_url_is_resolved(self):
        url = reverse('workout_linked_list')
        self.assertEquals(resolve(url).func, workoutLinkedListView)

    def test_workout_summary_url_is_resolved(self):
        url = reverse('workout_summary')
        self.assertEquals(resolve(url).func, workoutSummary)

    def test_workout_achievement_url_is_resolved(self):
        url = reverse('achievements')
        self.assertEquals(resolve(url).func, achievementsView)

    def test_leaderboard_url_is_resolved(self):
        url = reverse('leaderboards')
        self.assertEquals(resolve(url).func, Leaderboard)

    def test_changeUsername_url_is_resolved(self):
        url = reverse('change_username')
        self.assertEquals(resolve(url).func, changeUsername)

    def test_changeZipcode_url_is_resolved(self):
        url = reverse('change_zipcode')
        self.assertEquals(resolve(url).func, changeZipcode)

    def test_addModularWorkout_url_is_resolved(self):
        url = reverse('add_workout_modular')
        self.assertEquals(resolve(url).func, addModularWorkout)

    def test_addworkoutchoosetype_url_is_resolved(self):
        url = reverse('add_workout_choose_type')
        self.assertEquals(resolve(url).func, chooseTypeAddModularWorkout)