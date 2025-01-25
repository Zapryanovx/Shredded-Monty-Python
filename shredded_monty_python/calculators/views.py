from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required   
from .forms import OneRepMaxForm, BMIForm, CalorieForm, BodyFatForm
from .models import OneRepMaxLog, BMILog, CalorieLog, BodyFatLog
from django.utils.timezone import now
from django.apps import apps

@login_required
def calculators_view(request):
    return render(request, 'calculators_page.html')

@login_required
def one_rep_max_view(request):
    result = None
    logs = OneRepMaxLog.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = OneRepMaxForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            repetitions = form.cleaned_data['repetitions']
            exercise = form.cleaned_data['exercise']
            
            # Epley formula
            result = weight * (1 + repetitions / 30)
            
            if 'add_log' in request.POST:
                OneRepMaxLog.objects.create(
                    user=request.user,
                    exercise=exercise,
                    result=result,
                    date=now()
                )
                return redirect('one_rep_max')
    else:
        form = OneRepMaxForm()

    return render(request, 'calculators/one_rep_max.html', {
        'form': form,
        'result': result,
        'logs': logs
    })
    
@login_required
def bmi_view(request):
    result = None
    category = None
    logs = BMILog.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height'] / 100 
            weight = form.cleaned_data['weight']
            
            if height == 0:
                height = 1
                
            #BMI Fornula
            result = weight / (height ** 2)

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

        elif 'remove_log' in request.POST:
            log_id = request.POST.get('log_id')
            log = BMILog.objects.filter(id=log_id, user=request.user).first()
            if log:
                log.delete()
            return redirect('bmi')

    else:
        form = BMIForm()

    return render(request, 'calculators/bmi.html', {
        'form': form,
        'result': result,
        'category': category,
        'logs': logs
    })

@login_required
def calorie_view(request):
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

            # Mifflin-St Jeor Equation
            if gender == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            # Adjust BMR based on activity level
            activity_multipliers = {
                'sedentary': 1.2,
                'light': 1.375,
                'moderate': 1.55,
                'active': 1.725,
                'very_active': 1.9,
            }
            
            result = bmr * activity_multipliers[activity_level]

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
    result = None
    logs = BodyFatLog.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = BodyFatForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            height = form.cleaned_data['height'] / 100  # cm
            weight = form.cleaned_data['weight']

            if height == 0:
                height = 1
                
            bmi = weight / (height ** 2)

            if gender == 'male':
                result = 1.20 * bmi + 0.23 * age - 16.2
            elif gender == 'female':
                result = 1.20 * bmi + 0.23 * age - 5.4

            if result is not None and 'add_log' in request.POST:
                BodyFatLog.objects.create(
                    user=request.user,
                    gender=gender,
                    age=age,
                    height=height * 100,  # cm
                    weight=weight,
                    body_fat_percentage=result,
                    date=now()
                )
                return redirect('body_fat')
    else:
        form = BodyFatForm()

    return render(request, 'calculators/body_fat.html', {
        'form': form,
        'result': result,
        'logs': logs
    })
    
@login_required
def remove_log(request, log_type):
    if request.method == 'POST':
        log_id = request.POST.get('log_id')    
        model = apps.get_model('calculators', log_type)
        log = model.objects.filter(id=log_id, user=request.user).first()
    
        if log:
            log.delete()
    
    if log_type == 'OneRepMaxLog':
        return redirect('one_rep_max')
    elif log_type == 'BMILog':
        return redirect('bmi')
    elif log_type == 'CalorieLog':
        return redirect('calorie')
    elif log_type == 'BodyFatLog':
        return redirect('body_fat')
    else:
        return redirect('homepage') #[?] default
