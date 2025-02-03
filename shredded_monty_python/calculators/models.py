from django.db import models
from django.contrib.auth.models import User


class OneRepMaxLog(models.Model):
    EXERCISE_CHOICES = [
        ('bench_press', 'Bench Press'),
        ('squat', 'Squat'),
        ('deadlift', 'Deadlift'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=100, choices=EXERCISE_CHOICES)
    result = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
        
        
class BMILog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    bmi_result = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    

class CalorieLog(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'), ('female', 'Female')
    ]
    EXERCISE_ACTIVITY = [
        ('sedentary', 'Sedentary'),
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('active', 'Active'),
        ('very_active', 'Very Active'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    activity_level = models.CharField(max_length=20, choices=EXERCISE_ACTIVITY)
    calories = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    

class BodyFatLog(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'), ('female', 'Female')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    body_fat_percentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)