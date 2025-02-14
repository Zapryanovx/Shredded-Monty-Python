from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Exercise, WorkoutSession, Rating
from .forms import ExerciseForm, WorkoutSessionForm


class ExerciseModelTest(TestCase):
    """Tests for the Exercise model."""

    def test_create_exercise(self):
        """Tests if an exercise can be created successfully."""
        exercise = Exercise.objects.create(
            name="Push-Ups",
            muscle_group="chest",
            difficulty="beginner",
            optimal_sets_reps="3x15"
        )
        self.assertEqual(exercise.name, "Push-Ups")
        self.assertEqual(exercise.muscle_group, "chest")
        self.assertEqual(exercise.difficulty, "beginner")


class WorkoutSessionModelTest(TestCase):
    """Tests for the WorkoutSession model."""

    def setUp(self):
        self.exercise = Exercise.objects.create(
            name="Squats",
            muscle_group="legs",
            difficulty="beginner",
            optimal_sets_reps="4x12"
        )

    def test_create_session(self):
        """Tests if a workout session can be created and linked with exercises."""
        session = WorkoutSession.objects.create(
            name="Leg Day",
            description="Focus on legs"
        )
        session.exercises.add(self.exercise)
        self.assertIn(self.exercise, session.exercises.all())


class RatingModelTest(TestCase):
    """Tests for the Rating model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.exercise = Exercise.objects.create(
            name="Plank",
            muscle_group="core",
            difficulty="beginner",
            optimal_sets_reps="2x1 min"
        )

    def test_rating_creation(self):
        """Tests if a rating can be created and the average rating is updated."""
        Rating.objects.create(exercise=self.exercise, user=self.user, score=5)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.rating, 5.0)


class ExerciseFormTest(TestCase):
    """Tests for the Exercise form."""

    def test_valid_exercise_form(self):
        """Tests if the exercise form is valid with correct data."""
        form_data = {
            'name': 'Deadlift',
            'muscle_group': 'back',
            'difficulty': 'advanced',
            'optimal_sets_reps': '5x5',
            'video_url': 'https://example.com',
        }
        form = ExerciseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_exercise_form(self):
        """Tests if the exercise form is invalid with missing required fields."""
        form_data = {'name': ''}
        form = ExerciseForm(data=form_data)
        self.assertFalse(form.is_valid())


class WorkoutSessionFormTest(TestCase):
    """Tests for the WorkoutSession form."""

    def setUp(self):
        self.exercise = Exercise.objects.create(
            name="Lunges",
            muscle_group="legs",
            difficulty="intermediate",
            optimal_sets_reps="3x20"
        )

    def test_valid_workout_session_form(self):
        """Tests if the workout session form is valid."""
        form_data = {
            'name': 'Full Body',
            'description': 'A complete workout',
            'exercises': [self.exercise.id]
        }
        form = WorkoutSessionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_workout_session_form(self):
        """Tests if the workout session form is invalid without exercises."""
        form_data = {'name': 'Quick Session', 'description': 'No exercises selected'}
        form = WorkoutSessionForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    """Tests for the application views."""

    def setUp(self):
        """Create a test user and log in."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # make the user a superuser for access to delete views
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        
        self.client.login(username='testuser', password='testpassword')

        self.exercise = Exercise.objects.create(name='Push-up', muscle_group='chest', difficulty='beginner')
        self.session = WorkoutSession.objects.create(name='Morning Workout')

    def test_add_exercise_view_post(self):
        """Tests adding a new exercise via POST."""
        response = self.client.post(reverse('add_exercise'), {
            'name': 'Pull-Ups',
            'muscle_group': 'back',
            'difficulty': 'advanced',
            'optimal_sets_reps': '3x10'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Exercise.objects.filter(name='Pull-Ups').exists())

    def test_edit_exercise_view_post(self):
        """Tests editing an existing exercise via POST."""
        response = self.client.post(reverse('edit_exercise', args=[self.exercise.id]), {
            'name': 'Modified Push-Ups',
            'muscle_group': 'chest',
            'difficulty': 'beginner',
            'optimal_sets_reps': '3x20'
        })
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.name, 'Modified Push-Ups')

    def test_delete_exercise_view(self):
        """Tests deleting an exercise."""
        response = self.client.post(reverse('delete_exercise', args=[self.exercise.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Exercise.objects.filter(id=self.exercise.id).exists())

    def test_add_session_view_post(self):
        """Tests adding a workout session via POST."""
        response = self.client.post(reverse('add_session'), {
            'name': 'Morning Routine',
            'description': 'Quick start',
            'exercises': [self.exercise.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WorkoutSession.objects.filter(name='Morning Routine').exists())

    def test_delete_session_view(self):
        """Tests deleting a workout session."""
        response = self.client.post(reverse('delete_session', args=[self.session.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WorkoutSession.objects.filter(id=self.session.id).exists())

    def test_rate_exercise_view(self):
        """Tests rating an exercise."""
        response = self.client.post(reverse('rate_exercise', args=[self.exercise.id, 4]))
        self.exercise.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.exercise.rating, 4.0)
