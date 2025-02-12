from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.apps import apps
from .forms import OneRepMaxForm, BMIForm, CalorieForm, BodyFatForm
from .models import OneRepMaxLog, BMILog, CalorieLog, BodyFatLog


@login_required
def calculators_view(request):
    """Display the main page for fitness calculators."""
    return render(request, 'calculators_page.html')


@login_required
def one_rep_max_view(request):
    """Calculate and log the One-Rep Max."""
    result = None
    logs = OneRepMaxLog.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = OneRepMaxForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            repetitions = form.cleaned_data['repetitions']
            exercise = form.cleaned_data['exercise']

            # Calculate One-Rep Max using the Epley formula
            result = weight * (1 + repetitions / 30)

            if 'add_log' in request.POST:
                OneRepMaxLog.objects.create(
                    user=request.user,
                    exercise=exercise,
                    result=result,
                    date=now()
                )
                return redirect('onerepmax')
    else:
        form = OneRepMaxForm()

    return render(request, 'calculators/one_rep_max.html', {
        'form': form,
        'result': result,
        'logs': logs,
    })


@login_required
def bmi_view(request):
    """Calculate and log the BMI."""
    result = None
    category = None
    logs = BMILog.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height'] / 100  # Convert cm to meters
            weight = form.cleaned_data['weight']
            result = weight / (height ** 2) if height > 0 else 0

            # Determine BMI category
            if result < 18.5:
                category = "Underweight"
            elif 18.5 <= result < 24.9:
                category = "Normal weight"
            elif 25 <= result < 29.9:
                category = "Overweight"
            else:
                category = "Obesity"

            if 'add_log' in request.POST:
                BMILog.objects.create(
                    user=request.user,
                    height=height * 100,  # cm
                    weight=weight,
                    bmi_result=result,
                    date=now()
                )
                return redirect('bmi')
    else:
        form = BMIForm()

    return render(request, 'calculators/bmi.html', {
        'form': form,
        'result': result,
        'category': category,
        'logs': logs,
    })


@login_required
def calorie_view(request):
    """Calculate and log daily calorie needs."""
    result = None
    logs = CalorieLog.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = CalorieForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            activity_level = form.cleaned_data['activity_level']

            # Calculate BMR using Mifflin-St Jeor Equation
            bmr = (
                10 * weight + 6.25 * height - 5 * age + (5 if gender == 'male' else -161)
            )

            # Adjust BMR based on activity level
            activity_multipliers = {
                'sedentary': 1.2,
                'light': 1.375,
                'moderate': 1.55,
                'active': 1.725,
                'very_active': 1.9,
            }
            result = bmr * activity_multipliers.get(activity_level, 1)

            if 'add_log' in request.POST:
                CalorieLog.objects.create(
                    user=request.user,
                    gender=gender,
                    age=age,
                    height=height,
                    weight=weight,
                    activity_level=activity_level,
                    calories=result,
                    date=now()
                )
                return redirect('calorie')
    else:
        form = CalorieForm()

    return render(request, 'calculators/calorie_calculator.html', {
        'form': form,
        'result': result,
        'logs': logs,
    })


@login_required
def body_fat_view(request):
    """Calculate and log the body fat percentage."""
    result = None
    logs = BodyFatLog.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = BodyFatForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            height = form.cleaned_data['height'] / 100  # Convert cm to meters
            weight = form.cleaned_data['weight']

            bmi = weight / (height ** 2) if height > 0 else 0

            # Calculate body fat percentage
            if gender == 'male':
                result = 1.20 * bmi + 0.23 * age - 16.2
            elif gender == 'female':
                result = 1.20 * bmi + 0.23 * age - 5.4

            if 'add_log' in request.POST:
                BodyFatLog.objects.create(
                    user=request.user,
                    gender=gender,
                    age=age,
                    height=height * 100,  # cm
                    weight=weight,
                    body_fat_percentage=result,
                    date=now()
                )
                return redirect('bodyfat')
    else:
        form = BodyFatForm()

    return render(request, 'calculators/body_fat.html', {
        'form': form,
        'result': result,
        'logs': logs,
    })


@login_required
def remove_log(request, log_type):
    """Remove a log entry for a specified calculator log type."""
    if request.method == 'POST':
        log_id = request.POST.get('log_id')
        model = apps.get_model('calculators', log_type)
        log = model.objects.filter(id=log_id, user=request.user).first()
        if log:
            log.delete()

    return redirect(log_type.lower().replace("log", ""))
