from django.shortcuts import render, get_object_or_404, redirect
from .models import Exercise, Rating, WorkoutSession
from django.contrib.auth.decorators import login_required
from .forms import ExerciseForm, WorkoutSessionForm
from django.db.models import Q


def workouts(request):
    exercises = Exercise.objects.all()
    sessions = WorkoutSession.objects.prefetch_related('exercises').all()

    search_query = request.GET.get('search', '')
    if search_query:
        exercises = exercises.filter(
            Q(name__icontains=search_query) |
            Q(muscle_group__icontains=search_query)
        )

    muscle_group = request.GET.get('muscle_group', '')
    if muscle_group:
        exercises = exercises.filter(muscle_group__iexact=muscle_group)

    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        exercises = exercises.filter(difficulty__iexact=difficulty)
        
    sort_order = request.GET.get('sort', '')
    if sort_order == 'name_asc':
        exercises = exercises.order_by('name')
    elif sort_order == 'name_desc':
        exercises = exercises.order_by('-name')

    for exercise in exercises:
        exercise.user_has_rated = exercise.ratings.filter(user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'workouts.html', {'sessions': sessions, 'exercises': exercises})

@login_required
def rate_exercise(request, exercise_id, score):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    Rating.objects.update_or_create(
        exercise=exercise,
        user=request.user,
        defaults={'score': score},
    )
    exercise.update_rating()
    return redirect('workouts')

@login_required
def add_session(request):
    exercises = Exercise.objects.all() 
    if not request.user.is_superuser:
        return redirect('workouts')

    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workouts')
    else:
        form = WorkoutSessionForm()

        return render(request, 'add_session.html', {'form': form, 'exercises': exercises})

def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('workouts')
    else:
        form = ExerciseForm()
    return render(request, 'add_exercise.html', {'form': form})

def edit_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('workouts')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'edit_exercise.html', {'form': form, 'exercise': exercise})

@login_required
def delete_exercise(request, exercise_id):
    if not request.user.is_superuser:
        return redirect('workouts')
    
    exercise = get_object_or_404(Exercise, id=exercise_id)
    exercise.delete()
    return redirect('workouts')
