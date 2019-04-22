from django.urls import path

from .views import (
    subject_list,
    subject_create,
    subject_detail,
    subject_update,
    subject_delete,
)

app_name = 'course'
urlpatterns = [
    path('', subject_list, name='list'),
    path('create/', subject_create, name='create'),
    path('<int:id>/', subject_detail, name='detail'),
    path('<int:id>/edit/', subject_update, name='update'),
    path('<int:id>/delete/', subject_delete, name='delete'),
]
