from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Event(models.Model):
    """
    Model to represent an event with a title, description, and date.
    """
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()


class WaterLog(models.Model):
    """
    Model to track water intake logs for a user, including date, time, and amount.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    amount = models.PositiveIntegerField()
    time = models.TimeField(default=datetime.now)


class WorkoutLog(models.Model):
    """
    Model to track workout logs for a user, including exercise details and date.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    exercise = models.CharField(max_length=255)
    reps = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)


class WeightLog(models.Model):
    """
    Model to track weight logs for a user, including date, time, and weight.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.TimeField(default=datetime.now)
