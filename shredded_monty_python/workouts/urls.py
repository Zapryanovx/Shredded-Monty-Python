from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


"""
URL configuration for the application.

Routes:
- '' (root): Maps to `workouts`.
- 'add/': Maps to `add_exercise`.
- 'edit/<int:exercise_id>/': Maps to `edit_exercise`.
- 'delete/<int:exercise_id>/': Maps to `delete_exercise`.
- 'add_session/': Maps to `add_session`.
- 'edit_session/<int:session_id>/': Maps to `edit_session`.
- 'delete_session/<int:session_id>/': Maps to `delete_session`.
- 'rate/<int:exercise_id>/<int:score>/': Maps to `rate_exercise`.

"""

urlpatterns = [
    path('', views.workouts, name='workouts'),
    path('add/', views.add_exercise, name='add_exercise'),
    path('edit/<int:exercise_id>/', views.edit_exercise, name='edit_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('add_session/', views.add_session, name='add_session'),
    path('edit_session/<int:session_id>/', views.edit_session, name='edit_session'),
    path('delete_session/<int:session_id>/', views.delete_session, name='delete_session'),
    path('rate/<int:exercise_id>/<int:score>/', views.rate_exercise, name='rate_exercise'),
]

# If DEBUG mode is enabled, add URLs for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)