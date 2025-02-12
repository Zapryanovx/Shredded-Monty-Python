from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import OneRepMaxLog, BMILog, CalorieLog, BodyFatLog
from .forms import OneRepMaxForm, BMIForm, CalorieForm, BodyFatForm


class OneRepMaxFormTest(TestCase):
    """Test cases for One-Rep Max form."""

    def test_valid_form(self):
        """Checks if a valid form is accepted."""
        form_data = {'weight': 100, 'repetitions': 5, 'exercise': 'bench_press'}
        form = OneRepMaxForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Checks if an invalid form (negative weight) is rejected."""
        form_data = {'weight': -50, 'repetitions': 5, 'exercise': 'squat'}
        form = OneRepMaxForm(data=form_data)
        self.assertFalse(form.is_valid())


class BMIFormTest(TestCase):
    """Test cases for BMI form."""

    def test_valid_form(self):
        """Checks if a valid BMI form is accepted."""
        form_data = {
            'height': 180, 
            'weight': 75
        }
        form = BMIForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Checks if a BMI form with zero height is rejected."""
        form_data = {
            'height': 0,
            'weight': 75
        }
        form = BMIForm(data=form_data)
        self.assertFalse(form.is_valid())


class CalorieFormTest(TestCase):
    """Test cases for Calorie form."""

    def test_valid_form(self):
        """Checks if a valid Calorie form is accepted."""
        form_data = {
            'gender': 'male',
            'age': 25,
            'height': 175,
            'weight': 70,
            'activity_level': 'moderate'
        }
        form = CalorieForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Checks if an invalid Calorie form (negative age) is rejected."""
        form_data = {
            'gender': 'female',
            'age': -5,  # invalid age
            'height': 165,
            'weight': 60,
            'activity_level': 'light'
        }
        form = CalorieForm(data=form_data)
        self.assertFalse(form.is_valid())


class BodyFatFormTest(TestCase):
    """Test cases for Body Fat Percentage form."""

    def test_valid_form(self):
        """Checks if a valid Body Fat form is accepted."""
        form_data = {
            'gender': 'male', 
            'age': 30, 
            'height': 180, 
            'weight': 85
        }
        form = BodyFatForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Checks if an invalid Body Fat form (negative height) is rejected."""
        form_data = {
            'gender': 'female', 
            'age': 25, 
            'height': -160, 
            'weight': 55
        }
        form = BodyFatForm(data=form_data)
        self.assertFalse(form.is_valid())


class ModelsTest(TestCase):
    """Tests for log models."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_one_rep_max_log_creation(self):
        """Tests if One-Rep Max log is created correctly."""
        log = OneRepMaxLog.objects.create(user=self.user, exercise='bench_press', result=100)
        self.assertEqual(log.user.username, 'testuser')
        self.assertEqual(log.exercise, 'bench_press')

    def test_bmi_log_creation(self):
        """Tests if BMI log is created correctly."""
        log = BMILog.objects.create(user=self.user, height=180, weight=75, bmi_result=23.1)
        self.assertEqual(log.user.username, 'testuser')
        self.assertEqual(log.bmi_result, 23.1)

    def test_calorie_log_creation(self):
        """Tests if Calorie log is created correctly."""
        log = CalorieLog.objects.create(user=self.user, gender='male', age=25, height=175, weight=70, activity_level='moderate', calories=2500)
        self.assertEqual(log.user.username, 'testuser')
        self.assertEqual(log.calories, 2500)

    def test_body_fat_log_creation(self):
        """Tests if Body Fat log is created correctly."""
        log = BodyFatLog.objects.create(user=self.user, gender='male', age=30, height=180, weight=85, body_fat_percentage=18.5)
        self.assertEqual(log.user.username, 'testuser')
        self.assertEqual(log.body_fat_percentage, 18.5)


class ViewsTest(TestCase):
    """Tests for all calculator views including edge cases and form validation."""

    def setUp(self):
        """Set up test client and a test user."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_calculators_page(self):
        """Test if the main calculators page loads."""
        response = self.client.get(reverse('calculators'))
        self.assertEqual(response.status_code, 200)

    # One-Rep Max View Tests
    def test_one_rep_max_view_get(self):
        """Test if One-Rep Max page loads on GET request."""
        response = self.client.get(reverse('onerepmax'))
        self.assertEqual(response.status_code, 200)

    def test_one_rep_max_valid_post(self):
        """Test valid One-Rep Max form submission."""
        response = self.client.post(reverse('onerepmax'), {
            'weight': 100,
            'repetitions': 5,
            'exercise': 'bench_press',
            'calculate': 'true'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your One-Rep Max is")

    def test_one_rep_max_invalid_post(self):
        """Test invalid One-Rep Max form submission."""
        response = self.client.post(reverse('onerepmax'), {
            'weight': -10,  # invalid weight
            'repetitions': 5,
            'exercise': 'bench_press'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weight must be a positive number.")

    def test_one_rep_max_add_log(self):
        """Test adding a log for One-Rep Max."""
        response = self.client.post(reverse('onerepmax'), {
            'weight': 100,
            'repetitions': 5,
            'exercise': 'bench_press',
            'add_log': 'true'
        })
        self.assertEqual(response.status_code, 302)  # should redirect
        self.assertTrue(OneRepMaxLog.objects.filter(user=self.user).exists())

    # BMI View Tests
    def test_bmi_view_get(self):
        """Test if BMI page loads on GET request."""
        response = self.client.get(reverse('bmi'))
        self.assertEqual(response.status_code, 200)

    def test_bmi_valid_post(self):
        """Test valid BMI form submission."""
        response = self.client.post(reverse('bmi'), {
            'height': 180,
            'weight': 75
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your BMI is")

    def test_bmi_invalid_post(self):
        """Test invalid BMI form submission."""
        response = self.client.post(reverse('bmi'), {
            'height': 0,  # invalid height
            'weight': 75
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Height must be a positive number.")

    # Calorie Calculator View Tests
    def test_calorie_view_get(self):
        """Test if Calorie calculator page loads."""
        response = self.client.get(reverse('calorie'))
        self.assertEqual(response.status_code, 200)

    def test_calorie_valid_post(self):
        """Test valid Calorie form submission."""
        response = self.client.post(reverse('calorie'), {
            'gender': 'male',
            'age': 25,
            'height': 175,
            'weight': 70,
            'activity_level': 'moderate'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your daily calorie need is")

    def test_calorie_invalid_post(self):
        """Test invalid Calorie form submission."""
        response = self.client.post(reverse('calorie'), {
            'gender': 'male',
            'age': -5,  # invalid age
            'height': 175,
            'weight': 70,
            'activity_level': 'moderate'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Age must be a positive number.")

    # Body Fat View Tests
    def test_body_fat_view_get(self):
        """Test if Body Fat calculator page loads."""
        response = self.client.get(reverse('bodyfat'))
        self.assertEqual(response.status_code, 200)

    def test_body_fat_valid_post(self):
        """Test valid Body Fat form submission."""
        response = self.client.post(reverse('bodyfat'), {
            'gender': 'male',
            'age': 30,
            'height': 180,
            'weight': 85
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Body Fat Percentage is")

    def test_body_fat_invalid_post(self):
        """Test invalid Body Fat form submission."""
        response = self.client.post(reverse('bodyfat'), {
            'gender': 'male',
            'age': 30,
            'height': -180,  # invalid height
            'weight': 85
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Height must be a positive number.")

    def test_remove_log(self):
        """Test if a user can remove a log entry."""
        log = OneRepMaxLog.objects.create(user=self.user, exercise='bench_press', result=100)
        response = self.client.post(reverse('remove_log', args=['OneRepMaxLog']), {'log_id': log.id})
        self.assertEqual(response.status_code, 302)  # should redirect
        self.assertFalse(OneRepMaxLog.objects.filter(id=log.id).exists())
