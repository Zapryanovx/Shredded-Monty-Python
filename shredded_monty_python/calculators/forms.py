from django import forms

class OneRepMaxForm(forms.Form):
    weight = forms.FloatField(
        label="Weight (kg)", 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter weight in kg'
        })
    )
    repetitions = forms.IntegerField(
        label="Repetitions", 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter number of repetitions'
        })
    )
    exercise = forms.ChoiceField(
        choices=[
            ('bench_press', 'Bench Press'),
            ('squat', 'Squat'),
            ('deadlift', 'Deadlift'),
        ],
        label="Exercise",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class BMIForm(forms.Form):
    height = forms.FloatField(
        label="Height (cm)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your height in cm'
        })
    )
    weight = forms.FloatField(
        label="Weight (kg)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your weight in kg'
        })
    )


class CalorieForm(forms.Form):
    GENDER_CHOICES = [
        ('male', 'Male'), ('female', 'Female')
    ]
        
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Light exercise (1-3 days per week)'),
        ('moderate', 'Moderate exercise (3-5 days per week)'),
        ('active', 'Active (6-7 days per week)'),
        ('very_active', 'Very active (hard exercise)'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your age'
        })
    )
    height = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter height in cm'
        })
    )
    weight = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter weight in kg'
        })
    )
    activity_level = forms.ChoiceField(
        choices=ACTIVITY_LEVEL_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class BodyFatForm(forms.Form):
    GENDER_CHOICES = [
        ('male', 'Male'), ('female', 'Female')
    ]
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'})
    )
    weight = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter weight in kg'})
    )
    height = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter height in cm'})
    )