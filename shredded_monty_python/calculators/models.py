from django.db import models
from django.contrib.auth.models import User


class OneRepMaxLog(models.Model):
    """
    Model to store logs for One-Rep Max calculations.
    Contains the user, exercise type, result and timestamp.
    """
    
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
    """
    Model to store logs for BMI calculations.
    Contains the user, height, weight, BMI result and timestamp.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    bmi_result = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class CalorieLog(models.Model):
    """
    Model to store logs for daily calorie need calculations.
    Includes user data, physical stats, activity level and calories calculated.
    """
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Light exercise'),
        ('moderate', 'Moderate exercise'),
        ('active', 'Active exercise'),
        ('very_active', 'Very active'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    calories = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class BodyFatLog(models.Model):
    """
    Model to store logs for body fat percentage calculations.
    Stores user data, physical stats and calculated body fat percentage.
    """
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    body_fat_percentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
