import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Flashcard, Stack, UserFlaschcardRelationship
from .forms import StackForm, NewCardsForm
from .serializers import falshcard_serializer


def flashcards(request, pk):
    json_data = falshcard_serializer(pk, request)
    context = {'json_data': json_data, 'pk': pk}
    return render(request, 'flashcard/flashcards.html', context)


def edit_flashcards(request, pk):
    json_data = falshcard_serializer(pk, request)
    context = {'json_data': json_data, 'pk': pk}
    return render(request, 'flashcard/edit_flashcards.html', context)


def stack_list_view(request):
    stacks = Stack.objects.all().order_by('-id')
    context = {'stacks': stacks}
    return render(request, 'flashcard/stack_list.html', context)


@login_required(login_url='users:login')
def create_new_stack(request):
    if request.method == 'POST':
        form = StackForm(request.POST)
        if form.is_valid:
            form.instance.creator = request.user
            form.save()
            return redirect('flashcard:stack_list_view')
    else:
        form = StackForm()
    
    context = {'form': form}
    return render(request, 'flashcard/create_new_stack.html', context)


def add_new_cards(request, stack_id):
    if request.method == 'POST':
        form = NewCardsForm(request.POST)
        if form.is_valid:
            data = form.data['new_cards']
            stack_instance = Stack.objects.get(pk=stack_id)

            for d in data.split(";"):
                try:
                    term, definition = map(str.strip, d.split("&"))
                    Flashcard.objects.create(term=term, definition=definition, stack=stack_instance)
                except ValueError as e:
                    messages.error(request, e)
                    return redirect('flashcard:add_new_cards', stack_id=stack_id)

            return redirect('flashcard:edit_flashcards', pk=stack_id)
    else:
        form = NewCardsForm()
    
    context = {'form': form}
    return render(request, 'flashcard/add_new_cards.html', context)


def json_new_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        stack_instance = Stack.objects.get(pk=data['stack'])
        Flashcard.objects.create(term=data['term'], definition=data['definition'], stack=stack_instance)
        return JsonResponse({'message': 'Data received successfully'}, status=200)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        card_id = data['card_id']
        user = request.user
        card_instance = Flashcard.objects.get(pk=card_id)
        UserFlaschcardRelationship.objects.get(user_id=user, flashcard_id=card_instance).change_known()
        return JsonResponse({'message': 'Data received successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
