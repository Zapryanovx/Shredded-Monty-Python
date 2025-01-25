from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_profile, name='view_profile'),
    path('progress/', views.progress, name='progress'),
    path('calendar/', views.calendar, name='calendar'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout_view, name='logout'),
]