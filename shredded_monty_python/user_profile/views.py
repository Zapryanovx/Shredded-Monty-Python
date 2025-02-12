import json
from datetime import datetime, timedelta
from calendar import monthrange, month_name

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Min

from .forms import UserSettingsForm, PasswordChangeForm, WaterLogForm, WorkoutLogForm, WeightLogForm
from .models import WaterLog, WorkoutLog, WeightLog


@login_required
def view_profile(request):
    """
    Render the profile view page.
    """
    return render(request, 'profile/view.html')


@login_required
def progress(request):
    """
    Render the progress page.
    """
    return render(request, 'profile/progress.html')


@login_required
def calendar(request):
    """
    Render the calendar page.
    """
    return render(request, 'profile/calendar.html')


@login_required
def settings_view(request):
    """
    Handle updating user settings including profile updates and password changes.
    """
    user = request.user
    profile = user.profile

    settings_form = UserSettingsForm(
        request.POST or None,
        request.FILES or None,
        initial={'username': user.username, 'email': user.email}
    )
    password_form = PasswordChangeForm(request.POST or None)

    if request.method == 'POST':
        if 'save_profile' in request.POST and settings_form.is_valid():
            user.username = settings_form.cleaned_data['username']
            user.email = settings_form.cleaned_data['email']
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            user.save()
            profile.save()
            return redirect('settings')

        if 'change_password' in request.POST and password_form.is_valid():
            current_password = password_form.cleaned_data['current_password']
            new_password = password_form.cleaned_data['new_password']
            confirm_password = password_form.cleaned_data['confirm_password']

            if not user.check_password(current_password):
                password_form.add_error(
                    'current_password', 'The current password is incorrect.'
                )
            elif new_password != confirm_password:
                password_form.add_error(
                    'confirm_password', 'New password and confirmation do not match.'
                )
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('settings')

    return render(request, 'settings.html', {
        'settings_form': settings_form,
        'password_form': password_form,
        'profile': profile,
    })


@login_required
def send_emails_view(request):
    """
    Handle sending emails to selected recipients with an optional attachment.
    """
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='shreddedmontypython@gmail.com',
            to=[recipient] if recipient != 'all'
               else [u.email for u in User.objects.all()]
        )

        if attachment:
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        email.send()
        return redirect('send_emails')

    users = User.objects.all()
    return render(request, 'send_emails.html', {'users': users})


@login_required
def logout_view(request):
    """
    Log the user out and redirect to the homepage.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage')


def adjust_month_year(month, year):
    """
    Adjust the month and year values for calendar navigation.
    """
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
    return month, year


@login_required
def calendar_view(request):
    """
    Render the calendar view and handle form submissions for water,
    workout, and weight logs.
    """
    year = request.GET.get('year')
    month = request.GET.get('month')
    try:
        year = int(year) if year else datetime.now().year
        month = int(month) if month else datetime.now().month
    except ValueError:
        year = datetime.now().year
        month = datetime.now().month

    month, year = adjust_month_year(month, year)
    num_days = monthrange(year, month)[1]
    first_weekday = datetime(year, month, 1).weekday()

    # Build the calendar grid (list of weeks)
    month_days = []
    week = [0] * first_weekday
    for day in range(1, num_days + 1):
        week.append(day)
        if len(week) == 7:
            month_days.append(week)
            week = []
    if week:
        week += [0] * (7 - len(week))
        month_days.append(week)

    # Get selected date
    selected_date = request.POST.get("selected_date") or request.GET.get("selected_date")

    water_form = WaterLogForm(request.POST or None)
    workout_form = WorkoutLogForm(request.POST or None)
    weight_form = WeightLogForm(request.POST or None)

    if request.method == "POST" and selected_date:
        if "add_water_log" in request.POST and water_form.is_valid():
            WaterLog.objects.create(
                user=request.user,
                date=selected_date,
                time=water_form.cleaned_data['time'],
                amount=water_form.cleaned_data['amount']
            )
            return HttpResponseRedirect(
                f"?year={year}&month={month}&selected_date={selected_date}"
            )

        if "add_workout_log" in request.POST and workout_form.is_valid():
            WorkoutLog.objects.create(
                user=request.user,
                date=selected_date,
                exercise=workout_form.cleaned_data['exercise'],
                reps=workout_form.cleaned_data['reps'],
                sets=workout_form.cleaned_data['sets'],
                weight=workout_form.cleaned_data['weight']
            )
            return HttpResponseRedirect(
                f"?year={year}&month={month}&selected_date={selected_date}"
            )

        if "add_weight_log" in request.POST and weight_form.is_valid():
            WeightLog.objects.create(
                user=request.user,
                date=selected_date,
                weight=weight_form.cleaned_data['weight']
            )
            return HttpResponseRedirect(
                f"?year={year}&month={month}&selected_date={selected_date}"
            )

    water_logs = WaterLog.objects.filter(user=request.user, date=selected_date) if selected_date else None
    workout_logs = WorkoutLog.objects.filter(user=request.user, date=selected_date) if selected_date else None
    weight_logs = WeightLog.objects.filter(user=request.user, date=selected_date) if selected_date else None

    return render(request, 'calendar.html',  {
        'month_days': month_days,
        'year': year,
        'month_number': month,
        'month_name': month_name[month],
        'selected_date': selected_date,
        'water_form': water_form,
        'workout_form': workout_form,
        'weight_form': weight_form,
        'water_logs': water_logs,
        'workout_logs': workout_logs,
        'weight_logs': weight_logs,
    })


def delete_water_log(request, log_id):
    """
    Delete a water log entry and redirect to the calendar.
    """
    if request.method == 'POST':
        log = get_object_or_404(WaterLog, id=log_id)
        log.delete()
    return redirect('calendar')


def delete_workout_log(request, log_id):
    """
    Delete a workout log entry and redirect to the calendar.
    """
    if request.method == 'POST':
        log = get_object_or_404(WorkoutLog, id=log_id)
        log.delete()
    return redirect('calendar')


def delete_weight_log(request, log_id):
    """
    Delete a weight log entry and redirect to the calendar.
    """
    if request.method == 'POST':
        log = get_object_or_404(WeightLog, id=log_id)
        log.delete()
    return redirect('calendar')


@login_required
def progress_view(request):
    """
    Generate data for water, weight, and workout graphs.
    """
    today = datetime.now().date()
    start_date_30_days = today - timedelta(days=29)
    start_date_12_months = today - timedelta(days=365)

    # Water data (last 30 days)
    water_logs = WaterLog.objects.filter(
        user=request.user, date__range=[start_date_30_days, today]
    )
    water_totals = water_logs.values('date').annotate(total=Sum('amount')).order_by('date')
    water_data = [
        {"x": log['date'].strftime("%Y-%m-%d"), "y": log['total']}
        for log in water_totals
    ]

    # Weight data (last 30 days)
    weight_logs = WeightLog.objects.filter(
        user=request.user, date__range=[start_date_30_days, today]
    )
    weight_minimums = weight_logs.values('date').annotate(min_weight=Min('weight')).order_by('date')
    weight_data = [
        {"x": log['date'].strftime("%Y-%m-%d"), "y": float(log['min_weight'])}
        for log in weight_minimums
    ]

    # Workout data (last 12 months)
    workout_logs = WorkoutLog.objects.filter(user=request.user, date__gte=start_date_12_months)
    workout_totals = (
        workout_logs.values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    workout_data = [
        {"x": log['date'].strftime("%Y-%m-%d"), "y": log['count']}
        for log in workout_totals
    ]

    return render(request, 'progress.html', {
        "water_data": json.dumps(water_data, indent=4),
        "weight_data": json.dumps(weight_data, indent=4),
        "workout_data": json.dumps(workout_data, indent=4),
    })


@login_required
def view_profile(request):
    """
    Display a page with four sections:
      - Profile Data
      - Liked Posts: Posts the current user has liked.
      - Saved Posts: Posts the current user has saved.
      - Authored Posts: Posts created by the current user.
    """
    
    liked_posts = Post.objects.filter(likes__user=request.user).order_by('-created_at').distinct()
    saved_posts = Post.objects.filter(saves__user=request.user).order_by('-created_at').distinct()
    authored_posts = Post.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'view_profile.html', {
        'liked_posts': liked_posts,
        'saved_posts': saved_posts,
        'authored_posts': authored_posts,
    })
