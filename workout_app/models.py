from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Workout(models.Model):
    steps = models.CharField(max_length=30)
    miles = models.CharField(max_length=30)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "steps: " + self.steps + " | miles: " + self.miles

