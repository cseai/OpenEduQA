# from django.contrib import admin
from django.urls import path

from .views import (
    exam_list,
    exam_create,
    exam_detail,
    exam_update,
    exam_delete,
)

app_name = 'exam'
urlpatterns = [
    path('', exam_list, name='list'),
    path('create/', exam_create, name='create'),
    path('<id>/', exam_detail, name='detail'),
    path('<id>/edit/', exam_update, name='update'),
    path('<id>/delete/', exam_delete),
    #
]
