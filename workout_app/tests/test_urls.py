from django.test import SimpleTestCase
from django.urls import reverse, resolve
from workout_app.views import index, workoutLinkedListView, newWorkoutType, newWorkoutLinked, newWorkoutTypeCount, achievementsView

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

    def test_add_workout_achievement(self):
        url = reverse('achievements')
        self.assertEquals(resolve(url).func, achievementsView)