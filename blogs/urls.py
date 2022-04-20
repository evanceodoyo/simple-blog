"""Defines URL patterns for blogs."""

from django.urls import path
from . import views 

app_name = 'blogs'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    # Page that shows all blog posts. 
    path('posts/', views.posts, name='posts'),
    # Detail/entry of a single blog post. 
    path('posts/<int:post_id>/', views.post, name='post'),
    # Page for adding a new post
    path('new_post/', views.new_post, name='new_post'),
    # Page for editing a post.
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # Deleting a post. 
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]