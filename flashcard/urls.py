from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'flashcard'

urlpatterns = [
    path('', views.stack_list_view, name='stack_list_view'),
    path('create-new-stack', views.create_new_stack, name='create_new_stack'),
    path('flashcards/<int:pk>/', views.flashcards, name='flashcards'),
    path('edit-flashcards/<int:pk>/', views.edit_flashcards, name='edit_flashcards'),
    path('json_request_view', csrf_exempt(views.json_request_view), name='json_request_view'),
]
