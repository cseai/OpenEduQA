from django.urls import path

from .views import (
    level_list,
    level_create,
    level_detail,
    level_update,
    level_delete,
)

app_name = 'level'
urlpatterns = [
    path('', level_list, name='list'),
    path('create/', level_create, name='create'),
    path('<int:id>/', level_detail, name='detail'),
    path('<int:id>/edit/', level_update, name='update'),
    path('<int:id>/delete/', level_delete, name='delete'),
]
