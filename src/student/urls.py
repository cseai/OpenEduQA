from django.urls import path

from .views import (
    student_list_view,
    student_profile_view,
    student_update_view,
    student_view,
)

app_name = 'student'
urlpatterns = [
    path('', student_list_view, name='studentlist'),
    path('profile/', student_profile_view, name='profile'),
    path('<id>/', student_view, name='student'),
    path('profile/edit/', student_update_view, name='update'),
]
