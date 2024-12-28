from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('calculators/', views.calculators_view, name='calculators'),
    path('calculators/one-rep-max/', views.one_rep_max_view, name='one_rep_max'),
    path('calculators/bmi/', views.bmi_view, name='bmi'),
    path('calculators/calorie/', views.calorie_view, name='calorie'),
    path('calculators/body-fat/', views.body_fat_view, name='body_fat'),
    path('remove-log/<str:log_type>/', views.remove_log, name='remove_log'),
]
