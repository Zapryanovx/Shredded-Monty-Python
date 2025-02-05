from django.urls import path
from . import views


"""
URL configuration for the application.

Routes:
- 'view/' : Maps to `view_profile`.
- 'progress/': Maps to `progress`.
- 'calendar/': Maps to `calendar`.
- 'send-emails/': Maps to `send_emails_view`.
- 'settings/': Maps to `settings_view`.
- 'logout/': Maps to `logout_view`.

"""

urlpatterns = [
    path('view/', views.view_profile, name='view_profile'),
    path('progress/', views.progress, name='progress'),
    path('calendar/', views.calendar, name='calendar'),
    path('send-emails/', views.send_emails_view, name='send_emails'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.logout_view, name='logout'),
]