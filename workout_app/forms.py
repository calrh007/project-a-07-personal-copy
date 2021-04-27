from django import forms
# from .models import Workout

from .models import WorkoutType, WorkoutLinked, WorkoutTypeCount, City

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

'''
class WorkoutLinkedForm(forms.ModelForm):
    class Meta:
        model = WorkoutLinked
        exclude = ['profile']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }
        labels = {
            'workoutType': 'Workout Type'
        }
'''

class ContactForm1(forms.Form):
    
    class Meta:
        model = WorkoutType
        exclude = ['profile', 'is_official_type']

    # profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    zipcode = forms.CharField(max_length=5)

    leave_message = forms.BooleanField(required=False)

class ContactForm2(forms.Form):
    start_date = forms.DateField()
    one_day = forms.BooleanField()
    end_date = forms.DateField()
    duration = forms.DurationField()

class ContactForm3(forms.Form):
    intensity = forms.CharField(
    )
    '''
    dist = MeasurementField(
        blank = True,
        measurement=Distance,
        unit_choices=(("mi", "mi"), ("km", "km"), ("ft", "ft"), ("m", "m"))
    )
    '''

class ContactForm4(forms.Form):
    raw_count = forms.IntegerField()
    second_raw_count = forms.IntegerField()
    raw_set = forms.IntegerField()
    raw_rep = forms.IntegerField()
    '''
    weight = MeasurementField(
        blank = True,
        measurement=Weight,
        unit_choices=(("lb", "lb"), ("kg", "kg"))
    )
    '''

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