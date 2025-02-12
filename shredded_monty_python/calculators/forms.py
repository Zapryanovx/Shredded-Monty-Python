from django import forms


class OneRepMaxForm(forms.Form):
    """
    Form to calculate the One-Rep Max for a specific exercise.
    Includes fields for weight lifted, number of repetitions and exercise type.
    """
    
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
    
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Weight must be a positive number.")
        return weight

    def clean_repetitions(self):
        repetitions = self.cleaned_data.get('repetitions')
        if repetitions <= 0:
            raise forms.ValidationError("Repetitions must be a positive number.")
        return repetitions


class BMIForm(forms.Form):
    """
    Form to calculate the Body Mass Index (BMI).
    Includes fields for height in cm and weight in kg.
    """
    
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
    
    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height <= 0:
            raise forms.ValidationError("Height must be a positive number.")
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Weight must be a positive number.")
        return weight


class CalorieForm(forms.Form):
    """
    Form to calculate daily calorie needs based on activity level.
    Includes fields for gender, age, height, weight and activity level.
    """
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
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
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age <= 0:
            raise forms.ValidationError("Age must be a positive number.")
        return age
    
    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height <= 0:
            raise forms.ValidationError("Height must be a positive number.")
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Weight must be a positive number.")
        return weight


class BodyFatForm(forms.Form):
    """
    Form to calculate body fat percentage.
    Includes fields for gender, age, weight and height.
    """
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
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
    weight = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter weight in kg'
        })
    )
    height = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter height in cm'
        })
    )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age <= 0:
            raise forms.ValidationError("Age must be a positive number.")
        return age
    
    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height <= 0:
            raise forms.ValidationError("Height must be a positive number.")
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Weight must be a positive number.")
        return weight
