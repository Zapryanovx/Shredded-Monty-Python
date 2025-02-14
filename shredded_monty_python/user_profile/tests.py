from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import WorkoutSession, Exercise, Rating
from .forms import WorkoutSessionForm, ExerciseForm


class WorkoutSessionModelTest(TestCase):
    """Tests for the WorkoutSession model."""

    def test_create_workout_session(self):
        """Tests if a workout session is created correctly."""
        session = WorkoutSession.objects.create(name="Test Session", description="Test Description")
        self.assertEqual(session.name, "Test Session")
        self.assertEqual(session.description, "Test Description")


class ExerciseModelTest(TestCase):
    """Tests for the Exercise model."""

    def test_create_exercise(self):
        """Tests if an exercise is created correctly."""
        exercise = Exercise.objects.create(name="Push-ups", muscle_group="chest", difficulty="beginner", optimal_sets_reps="3x12")
        self.assertEqual(exercise.name, "Push-ups")
        self.assertEqual(exercise.muscle_group, "chest")


class RatingModelTest(TestCase):
    """Tests for the Rating model."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.exercise = Exercise.objects.create(name="Squats", muscle_group="legs", difficulty="beginner", optimal_sets_reps="4x10")

    def test_create_rating(self):
        """Tests if a rating is created and updates exercise rating correctly."""
        rating = Rating.objects.create(exercise=self.exercise, user=self.user, score=5)
        self.assertEqual(rating.score, 5)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.rating, 5)


class WorkoutSessionFormTest(TestCase):
    """Tests for the WorkoutSessionForm."""

    def test_valid_workout_session_form(self):
        """Tests if a valid form is accepted."""
        form_data = {'name': "Test Session", 'description': "Test description"}
        form = WorkoutSessionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_workout_session_form(self):
        """Tests if an invalid form (missing name) is rejected."""
        form_data = {'description': "Test description"}
        form = WorkoutSessionForm(data=form_data)
        self.assertFalse(form.is_valid())


class ExerciseFormTest(TestCase):
    """Tests for the ExerciseForm."""

    def test_valid_exercise_form(self):
        """Tests if a valid form is accepted."""
        form_data = {'name': "Bench Press", 'muscle_group': "chest", 'difficulty': "intermediate", 'optimal_sets_reps': "4x12"}
        form = ExerciseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_exercise_form(self):
        """Tests if an invalid form (missing name) is rejected."""
        form_data = {'muscle_group': "chest", 'difficulty': "intermediate", 'optimal_sets_reps': "4x12"}
        form = ExerciseForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    """Tests for all views in the Workout app."""

    def setUp(self):
        """Set up test client and test user."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.exercise = Exercise.objects.create(name="Deadlift", muscle_group="back", difficulty="advanced", optimal_sets_reps="5x5")
        self.session = WorkoutSession.objects.create(name="Morning Workout", description="Full body workout")

    def test_workouts_view(self):
        """Tests if the workouts page loads correctly."""
        response = self.client.get(reverse('workouts'))
        self.assertEqual(response.status_code, 200)

    def test_add_exercise_valid(self):
        """Tests adding a new exercise with valid data."""
        response = self.client.post(reverse('add_exercise'), {
            'name': 'Pull-ups', 'muscle_group': 'back', 'difficulty': 'intermediate', 'optimal_sets_reps': '3x10'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Exercise.objects.filter(name='Pull-ups').exists())

    def test_add_exercise_invalid(self):
        """Tests adding a new exercise with invalid data (missing fields)."""
        response = self.client.post(reverse('add_exercise'), {'muscle_group': 'back'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_edit_exercise(self):
        """Tests editing an existing exercise."""
        response = self.client.post(reverse('edit_exercise', args=[self.exercise.id]), {
            'name': 'Updated Deadlift', 'muscle_group': 'back', 'difficulty': 'advanced', 'optimal_sets_reps': '5x5'
        })
        self.assertEqual(response.status_code, 302)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.name, 'Updated Deadlift')

    def test_delete_exercise(self):
        """Tests deleting an exercise."""
        response = self.client.post(reverse('delete_exercise', args=[self.exercise.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Exercise.objects.filter(id=self.exercise.id).exists())

    def test_add_session_valid(self):
        """Tests adding a new workout session."""
        response = self.client.post(reverse('add_session'), {'name': 'Evening Workout', 'description': 'Leg day session'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WorkoutSession.objects.filter(name='Evening Workout').exists())

    def test_edit_session(self):
        """Tests editing an existing workout session."""
        response = self.client.post(reverse('edit_session', args=[self.session.id]), {'name': 'Updated Session', 'description': 'Updated description'})
        self.assertEqual(response.status_code, 302)
        self.session.refresh_from_db()
        self.assertEqual(self.session.name, 'Updated Session')

    def test_delete_session(self):
        """Tests deleting a workout session."""
        response = self.client.post(reverse('delete_session', args=[self.session.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WorkoutSession.objects.filter(id=self.session.id).exists())

    def test_rate_exercise(self):
        """Tests rating an exercise."""
        response = self.client.post(reverse('rate_exercise', args=[self.exercise.id, 5]))
        self.assertEqual(response.status_code, 302)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.rating, 5)

    def test_protected_views_without_login(self):
        """Tests if an unauthenticated user is redirected from protected views."""
        self.client.logout()
        protected_views = ['add_exercise', 'edit_exercise', 'delete_exercise', 'add_session', 'edit_session', 'delete_session', 'rate_exercise']
        for view in protected_views:
            response = self.client.get(reverse(view, args=[self.exercise.id] if 'exercise' in view else [self.session.id]))
            self.assertEqual(response.status_code, 302)

    def test_invalid_url(self):
        """Tests if an invalid URL returns a 404 status."""
        response = self.client.get('/invalid-url/')
        self.assertEqual(response.status_code, 404)
