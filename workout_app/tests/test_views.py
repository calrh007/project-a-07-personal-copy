from django.test import TestCase, Client
from django.urls import reverse
from workout_app.models import WorkoutTypeCount, WorkoutType, WorkoutLinked
import json

class TestViews(TestCase):

    def setUpClient(self):
        self.client = Client()
        self.index_url = reverse('index')

    def test_index_GET(self):
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)

    def test_index_VIEW(self):
        response = self.client.get(reverse('index'))

        self.assertTemplateUsed(response, 'workout_app/index.html')

    def test_workoutLinkedListView_GET(self):
        response = self.client.get(reverse('workout_linked_list'))

        self.assertEquals(response.status_code, 302)

    def test_newWorkoutType_GET(self):
        response = self.client.get(reverse('add_workout_type'))

        self.assertEquals(response.status_code, 302)

    def test_newWorkoutLinked_GET(self):
        response = self.client.get(reverse('add_workout_type_count'))

        self.assertEquals(response.status_code, 302)

    def test_newWorkoutTypeCount_GET(self):
        response = self.client.get(reverse('workout_linked_list'))

        self.assertEquals(response.status_code, 302)
