from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Workout(models.Model):
    type = models.CharField(max_length=30, default='')
    duration = models.CharField(max_length=30, default='')
    intensity = models.CharField(max_length=30, default='')
    steps = models.CharField(max_length=30, default='')
    miles = models.CharField(max_length=30, default='')
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "type: " + self.type
    def get_absolute_url(self):
        return reverse('workout_list')

