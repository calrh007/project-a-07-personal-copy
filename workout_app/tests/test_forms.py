from django.test import SimpleTestCase
from workout_app.forms import WorkoutTypeForm
from workout_app.models import WorkoutType, WorkoutLinked, WorkoutTypeCount

class TestForms(SimpleTestCase):

    def test_WorkoutTypeForm_valid_data(self):

        form = WorkoutTypeForm({
            'model': WorkoutType,
            'exclude': ['profile', 'is_official_type']
        })

        self.assertFalse(form.is_valid())

    def test_WorkoutLinked_valid_data(self):

        form = WorkoutTypeForm({
            'model': WorkoutLinked,
            'exclude': ['profile']
        })

        self.assertFalse(form.is_valid())

    def test_WorkoutTypeCount_valid_data(self):

        form = WorkoutTypeForm({
            'model': WorkoutTypeCount,
            'exclude': ['profile']
        })

        self.assertFalse(form.is_valid())
