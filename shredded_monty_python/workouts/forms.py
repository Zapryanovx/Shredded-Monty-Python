from django import forms
from .models import WorkoutSession, Exercise


class WorkoutSessionForm(forms.ModelForm):
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = WorkoutSession
        fields = ['name', 'description', 'exercises']
        
        
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'muscle_group', 'difficulty', 'optimal_sets_reps', 'video_url', 'image']