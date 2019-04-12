# from django.contrib import admin
from django.urls import path

from .views import (
    comment_thread,
    comment_delete
)

app_name = 'comments'
urlpatterns = [
    path('<int:id>/', comment_thread, name='thread'),
    path('<int:id>/delete/', comment_delete, name='delete'),
    # path('(?P<id>\d+)/', comment_thread, name='thread'),
    # path('(?P<id>\d+)/delete/', comment_delete, name='delete'),
]
