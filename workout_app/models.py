from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Workout(models.Model):
    type = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)
    intensity = models.CharField(max_length=30)
    steps = models.CharField(max_length=30)
    miles = models.CharField(max_length=30)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "type: " + self.type + " | duration: " + self.duration + " | intensity: " + self.duration +  " | steps: " + self.steps + " | miles: " + self.miles
    def get_absolute_url(self):
        return reverse('workout_list')