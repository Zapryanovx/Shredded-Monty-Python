from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.contrib.auth.models import User


class WorkoutSession(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    exercises = models.ManyToManyField('Exercise', related_name='workout_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)

    MUSCLE_GROUP_CHOICES = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('legs', 'Legs'),
        ('arms', 'Arms'),
        ('shoulders', 'Shoulders'),
        ('core', 'Core'),
        ('cardio', 'Cardio'),
    ]
    muscle_group = models.CharField(
        max_length=15,
        choices=MUSCLE_GROUP_CHOICES,
        default='beginner'
    )

    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    difficulty = models.CharField(
        max_length=15,
        choices=DIFFICULTY_LEVELS,
        default='beginner'
    )

    optimal_sets_reps = models.CharField(max_length=20, help_text="Example: 4x12 (4 sets of 12 reps)")

    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Average rating from 0 to 5"
    )

    def update_rating(self):
        ratings = self.ratings.all()
        self.rating = sum(rating.score for rating in ratings) / ratings.count() if ratings.exists() else 0
        self.save()
        
    video_url = models.URLField(
        max_length=200,
        blank=True,
        validators=[URLValidator()],
        help_text="URL to a video guide"
    )
    
    image = models.ImageField(
        upload_to='exercise_images/',
        blank=True,
    )
        
        
class Rating(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate from 1 to 5"
    )

    class Meta:
        unique_together = ('exercise', 'user')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.exercise.update_rating()