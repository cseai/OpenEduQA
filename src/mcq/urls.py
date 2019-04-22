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
    mcq_add_form,
)

app_name = 'mcq'
urlpatterns = [
    # path('', index_page, name='index'),
    path('', mcq_list, name='list'),
    path('create/', mcq_create, name='create'),
    path('<int:id>/', mcq_detail, name='detail'),
    path('<int:id>/edit/', mcq_update, name='update'),
    path('<int:id>/delete/', mcq_delete),
    #
    # path('editor/', latex_editor, name='editor'),
    path('test/', mcq_add_form, name='test'),
]
