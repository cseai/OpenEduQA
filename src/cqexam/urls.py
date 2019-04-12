# from django.contrib import admin
from django.urls import path

from .views import (
    cqexam_list,
    cqexam_create,
    cqexam_detail,
    cqexam_update,
    cqexam_delete,
)

app_name = 'cqexam'
urlpatterns = [
    path('', cqexam_list, name='list'),
    path('create/', cqexam_create, name='create'),
    path('<id>/', cqexam_detail, name='detail'),
    path('<id>/edit/', cqexam_update, name='update'),
    path('<id>/delete/', cqexam_delete),
]
