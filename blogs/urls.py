"""Defines URL patterns for blogs."""

from django.urls import path
from .views import index, post_detail_view, posts, edit_post, new_post, delete_post

app_name = 'blogs'
urlpatterns = [
    path('', index, name='index'),
    path('posts/', posts, name='posts'),
    path('post/<slug:slug>', post_detail_view, name='post_detail'),
    path('new_post/', new_post, name='new_post'),
    path('edit_post/<slug:slug>/', edit_post, name='edit_post'),
    path('delete_post/<slug:slug>/', delete_post, name='delete_post'),
]