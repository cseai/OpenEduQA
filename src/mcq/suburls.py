# from django.contrib import admin
from django.urls import path

from .views import (
    subject_content_list,
    # content_create,
    # content_detail,
    # content_update,
    # content_delete,
)

app_name = 'content'
urlpatterns = [
    # path('', index_page, name='index'),
    path('subject/<int:id>/', subject_content_list, name='list'),
    # path('create/', content_create, name='create'),
    # path('<id>/', content_detail, name='detail'),
    # path('<id>/edit/', content_update, name='update'),
    # path('<id>/delete/', content_delete),
]
