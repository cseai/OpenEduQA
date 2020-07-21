from django.urls import path

from .views import (
    ArticleCreateAPIView,
    ArticleDeleteAPIView,
    ArticleDetailAPIView,
    ArticleListAPIView, 
    ArticleUpdateAPIView,
)

app_name = 'article-api'
urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='list'),
    path('create/', ArticleCreateAPIView.as_view(), name='create'),
    path('<slug>/', ArticleDetailAPIView.as_view(), name='detail'),
    path('<slug>/edit/', ArticleUpdateAPIView.as_view(), name='update'),
    path('<slug>/delete/', ArticleDeleteAPIView.as_view(), name='delete'),
]
