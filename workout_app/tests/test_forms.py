from django.test import SimpleTestCase, TestCase
from workout_app.forms import WorkoutTypeForm, UsernameChangeForm, ZipChangeForm, WorkoutLinkedForm, WorkoutTypeCountForm, CityForm
from workout_app.models import WorkoutType, WorkoutLinked, WorkoutTypeCount, Achievement, User, Profile, City

class TestForms(SimpleTestCase):

    def test_WorkoutTypeForm_valid_data(self):

        form = WorkoutTypeForm({
            'model': WorkoutType,
            'exclude': ['profile', 'is_official_type']
        })

        self.assertFalse(form.is_valid())

    def test_UsernameChangeForm_valid_data(self):

        form = UsernameChangeForm({
            'model': User,
            'fields': ['username']
        })

        self.assertFalse(form.is_valid())

    def test_ZipChangeForm_valid_data(self):

        form = ZipChangeForm({
            'model': Profile,
            'fields': ['zipcode']
        })

        self.assertFalse(form.is_valid())

    def test_WorkoutLinkedForm_valid_data(self):

        form = WorkoutLinkedForm({
            'model': WorkoutLinked,
            'exclude': ['profile'],
        })

        self.assertFalse(form.is_valid())

    def test_WorkoutTypeCount_valid_data(self):

        form = WorkoutTypeCountForm({
            'model': WorkoutTypeCount,
            'exclude': ['profile']
        })

        self.assertFalse(form.is_valid())

    def test_CityFormIs_valid_data(self):

        form = CityForm({
            'model': City,
            'fields': ['name'],
        })

        self.assertFalse(form.is_valid())
