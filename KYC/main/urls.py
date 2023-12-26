# main/urls.py
from django.urls import path
from .views import (
    DocumentCreateAPIView,
    DocumentListAPIView,
    DocumentRetrieveUpdateDestroyAPIView
)

app_name = 'main'


urlpatterns = [
    path('create/', DocumentCreateAPIView.as_view(), name='document-create'),
    path('list/', DocumentListAPIView.as_view(), name='document-list'),
    path('detail/<int:pk>/', DocumentRetrieveUpdateDestroyAPIView.as_view(), name='document-detail'),
]
