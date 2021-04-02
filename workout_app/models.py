from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django_measurement.models import MeasurementField
from measurement.measures import Distance, Weight
# from django.conf import settings
import datetime

# Create your models here.

# class Workout(models.Model):
#     type = models.CharField(max_length=30, default='', blank=True)
#     duration = models.CharField(max_length=30, default='', blank=True)
#     intensity = models.CharField(max_length=30, default='', blank=True)
#     steps = models.CharField(max_length=30, default='', blank=True)
#     miles = models.CharField(max_length=30, default='', blank=True)
#     profile = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return "type: " + self.type
#     def get_absolute_url(self):
#         return reverse('workout_list')

class WorkoutTypeCount(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type_name = models.CharField(max_length=30, default='')
    def __str__(self):
        return self.type_name

class WorkoutType(models.Model):
    type_name = models.CharField(max_length=30, default='')
    has_intensity = models.BooleanField(default=False)
    has_distance_comp = models.BooleanField(default=False)
    has_first_count_component = models.BooleanField(default=False)
    first_count_component = models.ForeignKey(WorkoutTypeCount, on_delete=models.CASCADE, null=True, blank=True)
    has_second_count_component = models.BooleanField(default=False)
    second_count_component = models.ForeignKey(WorkoutTypeCount, on_delete=models.CASCADE, related_name='second_cc', null=True, blank=True)
    has_set_rep_comp = models.BooleanField(default=False)
    has_weight_comp = models.BooleanField(default=False)
    is_official_type = models.BooleanField(default=False)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.type_name

INTENSITY_CHOICES = (
    ('L', 'Light'),
    ('M', 'Moderate'),
    ('V', 'Vigorous'),
    ('NA', 'Not Applicable')
)


class WorkoutLinked(models.Model):
    workoutType = models.ForeignKey(WorkoutType, on_delete=models.CASCADE)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=datetime.date.today)
    one_day = models.BooleanField(default=True)
    end_date = models.DateField(default=datetime.date.today)
    intensity = models.CharField(
        max_length = 2,
        choices = INTENSITY_CHOICES,
        default = 'L'
    )
    dist = MeasurementField(
        default=0,
        measurement=Distance,
        unit_choices=(("mi", "mi"), ("km", "km"), ("ft", "ft"), ("m", "m"))
    )

    raw_count = models.PositiveIntegerField(default = 0)
    second_raw_count = models.PositiveIntegerField(default = 0)
    raw_set = models.PositiveIntegerField(default = 0)
    raw_rep = models.PositiveIntegerField(default = 0)
    weight = MeasurementField(
        null=True,
        blank=True,
        default=0,
        measurement=Weight,
        unit_choices=(("lb", "lb"), ("kg", "kg"))
    )