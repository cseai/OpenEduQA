# from django.contrib import admin
from django.urls import path

from .views import (
    teacher_list_view,
    teacher_profile_view,
    teacher_update_view,
    teacher_view,
)

app_name = 'teacher'
urlpatterns = [
    path('', teacher_list_view, name='teacherlist'),
    path('profile/', teacher_profile_view, name='profile'),
    path('<id>/', teacher_view, name='teacher'),
    path('profile/edit/', teacher_update_view, name='update'),
]
