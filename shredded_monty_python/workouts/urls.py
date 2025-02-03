from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.workouts, name='workouts'),
    path('add/', views.add_exercise, name='add_exercise'),
    path('add_session/', views.add_session, name='add_session'),
    path('rate/<int:exercise_id>/<int:score>/', views.rate_exercise, name='rate_exercise'),
    path('edit/<int:exercise_id>/', views.edit_exercise, name='edit_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)