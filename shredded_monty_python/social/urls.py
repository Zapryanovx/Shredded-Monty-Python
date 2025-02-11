from django.urls import path
from . import views

urlpatterns = [
    path('', views.social_feed, name='social_feed'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('save/<int:post_id>/', views.save_post, name='save_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:post_id>/<int:parent_id>/', views.add_comment, name='reply_comment'),
]
