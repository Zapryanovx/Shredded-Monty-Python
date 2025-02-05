from django import forms
from .models import Exercise


class WorkoutSessionForm(forms.Form):
    """
    Form to create or update a workout session.
    Includes fields for session name, description and exercises selection.
    """
    
    name = forms.CharField(
        label="Session Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter session name'
        }),
        required=True
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter session description',
            'rows': 4
        }),
        required=False
    )
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label="Select Exercises",
        required=True
    )


class ExerciseForm(forms.Form):
    """
    Form to create or update an exercise.
    Includes fields for exercise name, muscle group, difficulty, optimal sets/reps, video URL and image upload.
    """
    
    name = forms.CharField(
        label="Exercise Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter exercise name'
        }),
        required=True
    )
    muscle_group = forms.ChoiceField(
        label="Muscle Group",
        choices=[
            ('chest', 'Chest'),
            ('back', 'Back'),
            ('legs', 'Legs'),
            ('arms', 'Arms'),
            ('shoulders', 'Shoulders'),
            ('core', 'Core'),
            ('cardio', 'Cardio'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    difficulty = forms.ChoiceField(
        label="Difficulty",
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    optimal_sets_reps = forms.CharField(
        label="Optimal Sets & Reps",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 3 sets of 10-12 reps'
        }),
        required=True
    )
    video_url = forms.URLField(
        label="Video URL",
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter video URL (optional)'
        }),
        required=False
    )
    image = forms.ImageField(
        label="Upload Image",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file'
        }),
        required=False
    )
