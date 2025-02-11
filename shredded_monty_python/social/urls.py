from django.urls import path
from . import views


"""
URL configuration for the application.

Routes:
- '' : Maps to `view_profile`.
- 'create/': Maps to `social_feed`.
- 'like/<int:post_id>/': Maps to `like_post`.
- 'save/<int:post_id>/': Maps to `save_post`.
- 'comment/<int:post_id>/': Maps to `add_comment`.
- 'comment/<int:post_id>/<int:parent_id>/': Maps to `reply_comment`.
- 'delete_post/<int:post_id>/': Maps to `delete_post`.
- 'delete_comment/<int:comment_id>/': Maps to `delete_comment`.

"""

urlpatterns = [
    path('', views.social_feed, name='social_feed'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('save/<int:post_id>/', views.save_post, name='save_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:post_id>/<int:parent_id>/', views.add_comment, name='reply_comment'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
