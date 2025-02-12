from django.urls import path
from . import views


"""
URL configuration for the application.

Routes:
- '' (root): Maps to `calculators_view`.
- 'one-rep-max/' : Maps to `one_rep_max_view`.
- 'bmi/' : Maps to `bmi_view`.
- 'calorie/' : Maps to `calorie_view`.
- 'body-fat/' : Maps to `body_fat_view`.
- 'remove-log/<str:log_type>/' : Maps to `remove_log`.
"""

urlpatterns = [
    path('', views.calculators_view, name='calculators'), 
    path('one-rep-max/', views.one_rep_max_view, name='onerepmax'),
    path('bmi/', views.bmi_view, name='bmi'),
    path('calorie/', views.calorie_view, name='calorie'),
    path('body-fat/', views.body_fat_view, name='bodyfat'),
    path('remove-log/<str:log_type>/', views.remove_log, name='remove_log'),
]
