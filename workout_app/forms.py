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