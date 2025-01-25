from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculators_view, name='calculators'),  # Главна страница на калкулаторите
    path('one-rep-max/', views.one_rep_max_view, name='one_rep_max'),
    path('bmi/', views.bmi_view, name='bmi'),
    path('calorie/', views.calorie_view, name='calorie'),
    path('body-fat/', views.body_fat_view, name='body_fat'),
    path('remove-log/<str:log_type>/', views.remove_log, name='remove_log'),
]
