from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'flashcard'

urlpatterns = [
    path('flashcard/<int:pk>/', views.flashcards, name='flashcard_view'),
    path('', views.flashcard_list_view, name='flashcard_list_view'),
    path('json_request_view', csrf_exempt(views.json_request_view), name='json_request_view'),
]
