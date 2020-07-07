from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # API to post a comment.
    path('postComment', views.postComment, name = 'postComment'),
    path('',views.blogHome,name='blogHome'),
    # '<str:slug>' is for posts of the blog app which we will fetch from database.
    # In url we write it as 127.0.0.1:8000/blog/<str:slug>
    path('<str:slug>',views.blogPost,name='blogPost'), 
    

]