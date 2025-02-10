from django.urls import path
from . import views


"""
URL configuration for the application.

Routes:
- 'view/' : Maps to `view_profile`.
- 'progress/': Maps to `progress`.
- 'calendar/': Maps to `calendar`.
- 'delete-water-log/<int:log_id>/': Maps to `delete_water_log`.
- 'delete-workout-log/<int:log_id>/': Maps to `delete_workout_log`.
- 'delete-weight-log/<int:log_id>/': Maps to `delete_weight_log`.
- 'send-emails/': Maps to `send_emails_view`.
- 'settings/': Maps to `settings_view`.
- 'logout/': Maps to `logout_view`.

"""

urlpatterns = [
    path('view/', views.view_profile, name='view_profile'),
    path('progress/', views.progress_view, name='progress'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('delete-water-log/<int:log_id>/', views.delete_water_log, name='delete_water_log'),
    path('delete-workout-log/<int:log_id>/', views.delete_workout_log, name='delete_workout_log'),
    path('delete-weight-log/<int:log_id>/', views.delete_weight_log, name='delete_weight_log'),
    path('send-emails/', views.send_emails_view, name='send_emails'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.logout_view, name='logout'),
]