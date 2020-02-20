from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='main_page_url'),

    path('posts/', posts_list, name='posts_list_url'),
    path('posts/create/', PostCreate.as_view(), name='post_create_url'),
    path('posts/<str:slug>/', detailed_post, name='detailed_post_url'),
    path('posts/<str:slug>/edit/', EditPost.as_view(), name='edit_post_url'),
    path('posts/<str:slug>/delete/', DeletePost.as_view(), name='delete_post_url'),
    path('post/<str:slug>/changed/', changed_post, name='changed_post_url'),

    path('tags/', tags_list, name='tags_list_url'),
    path('tags/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tags/<str:slug>/', detailed_tag, name='detailed_tag_url'),
    path('tags/<str:slug>/edit/', EditTag.as_view(), name='edit_tag_url'),
    path('tags/<str:slug>/delete/', DeleteTag.as_view(), name='delete_tag_url'),
    path('tag/<str:slug>/changed/', changed_tag, name='changed_tag_url'),
]
