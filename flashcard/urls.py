from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'flashcard'

urlpatterns = [
    path('', views.stack_list_view, name='stack_list_view'),
    path('my-cards', views.my_cards_view, name='my_cards_view'),
    path('create-new-stack', views.create_new_stack, name='create_new_stack'),
    path('flashcards/<int:stack_id>/', views.flashcards, name='flashcards'),
    path('edit-flashcards/<int:stack_id>/', views.edit_flashcards, name='edit_flashcards'),
    path('add-new-cards/<int:stack_id>/', views.add_new_cards, name="add_new_cards"),
    path('json-request-view', csrf_exempt(views.json_reciever), name='json_reciever'),
]
