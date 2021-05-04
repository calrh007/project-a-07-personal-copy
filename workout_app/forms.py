from django import forms
# from .models import Workout

from .models import WorkoutType, WorkoutLinked, WorkoutTypeCount, City
from django.contrib.auth.models import User

from .models import Profile

# class WorkoutForm(forms.ModelForm):
#     class Meta:
#         model = Workout
#         fields = ('type', 'duration', 'intensity', 'steps', 'miles', 'profile')

#         widgets = {
#             'type': forms.TextInput(attrs={'class': 'form-control'}),
#             'duration': forms.TextInput(attrs={'class': 'form-control'}),
#             'intensity': forms.TextInput(attrs={'class': 'form-control'}),
#             'steps': forms.TextInput(attrs={'class': 'form-control'}),
#             'miles': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.fields['profile'].queryset = Workout.objects.none()

class WorkoutTypeForm(forms.ModelForm):
    class Meta:
        model = WorkoutType
        exclude = ['profile', 'is_official_type']

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ZipChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['zipcode']


class WorkoutLinkedForm(forms.ModelForm):
    class Meta:
        model = WorkoutLinked
        exclude = ['profile']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }

class ChooseWorkoutTypeForm(forms.Form):
    workout_type = forms.ModelChoiceField(WorkoutType.objects.all())

class ModularWorkoutLinkedForm(forms.ModelForm):
    class Meta:
        model = WorkoutLinked
        exclude = ['profile', 'workoutType']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }
    def __init__(self, *args, **kwargs):
        self.workout_type_inp = kwargs.pop('workout_type')
        super(ModularWorkoutLinkedForm, self).__init__(*args, **kwargs)
        if not self.workout_type_inp.has_intensity:
            self.fields.pop('intensity')
        if not self.workout_type_inp.has_duration:
            self.fields.pop('duration')
        if not self.workout_type_inp.has_distance_comp:
            self.fields.pop('dist')
        if not self.workout_type_inp.has_first_count_component:
            self.fields.pop('raw_count')
        else:
            self.fields['raw_count'].label = self.workout_type_inp.first_count_component.type_name
        if not self.workout_type_inp.has_second_count_component:
            self.fields.pop('second_raw_count')
        else:
            self.fields['second_raw_count'].label = self.workout_type_inp.second_count_component.type_name
        if not self.workout_type_inp.has_set_rep_comp:
            self.fields.pop('raw_set')
            self.fields.pop('raw_rep')
        if not self.workout_type_inp.has_weight_comp:
            self.fields.pop('weight')

class WorkoutTypeCountForm(forms.ModelForm):
    class Meta:
        model = WorkoutTypeCount
        exclude = ['profile']

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder' : 'Zip Code'}),
        }