from django.urls import path

from .views import (
    article_list,
    article_create,
    article_detail,
    article_update,
    article_delete,
)

app_name = 'article'
urlpatterns = [
    path('', article_list, name='list'),
    path('create/', article_create, name='create'),
    path('<slug>/', article_detail, name='detail'),
    path('<slug>/edit/', article_update, name='update'),
    path('<slug>/delete/', article_delete),
]
