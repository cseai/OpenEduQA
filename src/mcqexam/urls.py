from django.urls import path

from .views import (
    mcqexam_list,
    mcqexam_create,
    mcqexam_detail,
    mcqexam_update,
    mcqexam_delete,
)

app_name = 'mcqexam'
urlpatterns = [
    path('', mcqexam_list, name='list'),
    path('create/', mcqexam_create, name='create'),
    path('<id>/', mcqexam_detail, name='detail'),
    path('<id>/edit/', mcqexam_update, name='update'),
    path('<id>/delete/', mcqexam_delete),
    #
]
