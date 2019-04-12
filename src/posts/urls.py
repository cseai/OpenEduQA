# from django.contrib import admin
from django.urls import path

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
)

app_name = 'posts'
urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create),
    path('<slug>/', post_detail, name='detail'),
    path('<slug>/edit/', post_update, name='update'),
    path('<slug>/delete/', post_delete),
    # path('(?P<slug>[\w-]+)/', post_detail, name='detail'),
    # path('(?P<slug>[\w-]+)/edit/', post_update, name='update'),
    # path('(?P<slug>[\w-]+)/delete/', post_delete),
    # path('posts/', "<appname>.views.<function_name>"),
]
