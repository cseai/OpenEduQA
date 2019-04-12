# from django.contrib import admin
from django.urls import path
from .views import room_list_view, room_detail, room_create, room_update_view, room_delete, datetime_view, CreateView

app_name = 'room'
urlpatterns = [
    path('', room_list_view, name='roomlist'),
    # path('create/', CreateView.as_view(), name='create'),
    path('create/', room_create, name='create'),
    path('<int:id>/', room_detail, name='detail'),
    path('<int:id>/edit/', room_update_view, name='update'),
    path('<int:id>/delete/', room_delete, name='delete'),
    path('test/', datetime_view, name='test'),
]
