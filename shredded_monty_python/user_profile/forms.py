from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserSettingsForm(forms.Form):
    """
    Form for updating user profile information and profile picture.
    """
    
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
        }),
        required=True
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        }),
        required=True
    )
    profile_picture = forms.ImageField(
        label="Profile Picture",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
        })
    )


class PasswordChangeForm(forms.Form):
    """
    Form for changing the user's password.
    """
    
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password',
        }),
        required=True
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password',
        }),
        required=True,
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
        }),
        required=True
    )

    def clean(self):
        """
        Ensure that the new password and confirmation match.
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise ValidationError("New password and confirm password do not match.")
        return cleaned_data


class WaterLogForm(forms.Form):
    """
    Form for adding water intake logs.
    """
    
    amount = forms.IntegerField(
        label="Water Intake (ml)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter water amount in ml'
        }),
        required=True
    )
    time = forms.TimeField(
        label="Time",
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter time (HH:MM)',
            'type': 'time'
        }),
        required=True
    )


class WorkoutLogForm(forms.Form):
    """
    Form for adding workout logs.
    """
    
    exercise = forms.CharField(
        label="Exercise",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter exercise name'
        }),
        required=True
    )
    reps = forms.IntegerField(
        label="Reps",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter number of repetitions'
        }),
        required=True
    )
    sets = forms.IntegerField(
        label="Sets",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter number of sets'
        }),
        required=True
    )
    weight = forms.FloatField(
        label="Weight (kg)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter weight used (kg)'
        }),
        required=True
    )


class WeightLogForm(forms.Form):
    """
    Form for adding weight logs.
    """
    
    weight = forms.FloatField(
        label="Weight (kg)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your weight (kg)'
        }),
        required=True
    )
    time = forms.TimeField(
        label="Time",
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter time (HH:MM)',
            'type': 'time'
        }),
        required=True
    )
