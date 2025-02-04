from django.urls import path
from . import views


"""
URL configuration for the application.

Routes:
- '' (root): Maps to `homepage_view`.
- 'register/': Maps to `register_view`.
- 'login/': Maps to `login_view`.
- 'contact/': Maps to `contact_view`.
"""

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact_view, name='contact'),
]
