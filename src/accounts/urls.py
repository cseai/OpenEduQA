# from django.contrib import admin
from django.urls import path
from .views import profile_view, profile_update_view, user_view, user_list_view

app_name = 'accounts'
urlpatterns = [
    path('users/', user_list_view, name='userlist'),
    path('user/', profile_view, name='profile'),
    path('user/<int:id>', user_view, name='user'),
    path('user/edit/', profile_update_view, name='profile_update'),
]
