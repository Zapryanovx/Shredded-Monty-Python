from django.shortcuts import render, get_object_or_404, redirect
from .models import Exercise, Rating, WorkoutSession
from django.contrib.auth.decorators import login_required
from .forms import ExerciseForm, WorkoutSessionForm
from django.db.models import Q


def workouts(request):
    """Display a list of exercises and workout sessions with filter functionality."""
    
    exercises = Exercise.objects.all()
    sessions = WorkoutSession.objects.prefetch_related('exercises').all()

    # Filtering and search functionality
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
        
    # Sorting functionality
    sort_order = request.GET.get('sort', '')
    if sort_order == 'name_asc':
        exercises = exercises.order_by('name')
    elif sort_order == 'name_desc':
        exercises = exercises.order_by('-name')

    # Check if user has rated the exercises
    for exercise in exercises:
        exercise.user_has_rated = exercise.ratings.filter(user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'workouts.html', {'sessions': sessions, 'exercises': exercises})


@login_required
def add_session(request):
    """
    View to add a new workout session.
    Displays a form where the user can input session details and select exercises.
    """
  
    exercises = Exercise.objects.all()
    
    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            workout_session = WorkoutSession.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description']
            )
            
            workout_session.exercises.set(form.cleaned_data['exercises'])
            return redirect('workouts')
    else:
        form = WorkoutSessionForm()

    return render(request, 'add_session.html', {'form': form, 'exercises': exercises})


@login_required
def edit_session(request, session_id):
    """Handle editing an existing session."""
    session = get_object_or_404(WorkoutSession, id=session_id)
    exercises = Exercise.objects.all()

    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST, initial={
            'name': session.name,
            'description': session.description,
            'exercises': exercises,
        })

        if form.is_valid():
            session.name = form.cleaned_data['name']
            session.description = form.cleaned_data['description']
            session.exercises.set(form.cleaned_data['exercises'])
            session.save()
            return redirect('workouts')
    else:
        form = WorkoutSessionForm(initial={
            'name': session.name,
            'description': session.description,
            'exercises': exercises,
        })

    return render(request, 'edit_session.html', {
        'form': form,
        'session': session,
        'exercises': exercises,
    })
    

@login_required
def delete_session(request, session_id):
    """Handle deleting a workout session."""
    if not request.user.is_superuser:
        return redirect('workouts')
    
    session = get_object_or_404(WorkoutSession, id=session_id)
    session.delete()
    return redirect('workouts')


def add_exercise(request):
    """Handle the creation of a new exercise."""
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            Exercise.objects.create(
                name=form.cleaned_data['name'],
                muscle_group=form.cleaned_data['muscle_group'],
                difficulty=form.cleaned_data['difficulty'],
                optimal_sets_reps=form.cleaned_data['optimal_sets_reps'],
                video_url=form.cleaned_data['video_url'],
                image=form.cleaned_data['image']
            )
            return redirect('workouts')
    else:
        form = ExerciseForm()
    return render(request, 'add_exercise.html', {'form': form})


def edit_exercise(request, exercise_id):
    """Handle editing an existing exercise."""
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            exercise.name = form.cleaned_data['name']
            exercise.muscle_group = form.cleaned_data['muscle_group']
            exercise.difficulty = form.cleaned_data['difficulty']
            exercise.optimal_sets_reps = form.cleaned_data['optimal_sets_reps']
            exercise.video_url = form.cleaned_data['video_url']
            if form.cleaned_data['image']:
                exercise.image = form.cleaned_data['image']
            exercise.save()
            return redirect('workouts')
    else:
        form = ExerciseForm(initial={
            'name': exercise.name,
            'muscle_group': exercise.muscle_group,
            'difficulty': exercise.difficulty,
            'optimal_sets_reps': exercise.optimal_sets_reps,
            'video_url': exercise.video_url,
            'image': exercise.image,
        })
    return render(request, 'edit_exercise.html', {'form': form, 'exercise': exercise})


@login_required
def delete_exercise(request, exercise_id):
    """Handle deleting an exercise."""
    if not request.user.is_superuser:
        return redirect('workouts')
    
    exercise = get_object_or_404(Exercise, id=exercise_id)
    exercise.delete()
    return redirect('workouts')


@login_required
def rate_exercise(request, exercise_id, score):
    """
    Handle the rating of an exercise by a user.
    Allows users to rate an exercise and updates the average rating.
    """

    exercise = get_object_or_404(Exercise, id=exercise_id)
    Rating.objects.update_or_create(
        exercise=exercise,
        user=request.user,
        defaults={'score': score},
    )

    exercise.update_rating()
    return redirect('workouts')
