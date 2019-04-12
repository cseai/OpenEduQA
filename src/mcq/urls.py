# from django.contrib import admin
from django.urls import path

from .views import (
    # index_page,
    mcq_list,
    # latex_editor,
    mcq_create,
    mcq_detail,
    mcq_update,
    mcq_delete,
)

app_name = 'mcq'
urlpatterns = [
    # path('', index_page, name='index'),
    path('', mcq_list, name='list'),
    path('create/', mcq_create, name='create'),
    path('<id>/', mcq_detail, name='detail'),
    path('<id>/edit/', mcq_update, name='update'),
    path('<id>/delete/', mcq_delete),
    #
    # path('editor/', latex_editor, name='editor'),
]
