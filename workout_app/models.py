from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Workout(models.Model):
    type = models.CharField(max_length=30, default='', blank=True)
    duration = models.CharField(max_length=30, default='', blank=True)
    intensity = models.CharField(max_length=30, default='', blank=True)
    steps = models.CharField(max_length=30, default='', blank=True)
    miles = models.CharField(max_length=30, default='', blank=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "type: " + self.type
    def get_absolute_url(self):
        return reverse('workout_list')

