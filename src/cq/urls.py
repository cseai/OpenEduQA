# from django.contrib import admin
from django.urls import path

from .views import (
    cq_list,
    cq_create,
    cq_detail,
    cq_update,
    cq_delete,
)

app_name = 'cq'
urlpatterns = [
    path('', cq_list, name='list'),
    path('create/', cq_create, name='create'),
    path('<id>/', cq_detail, name='detail'),
    path('<id>/edit/', cq_update, name='update'),
    path('<id>/delete/', cq_delete),
    #
]
