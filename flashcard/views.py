import json
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Flashcard, Stack, UserFlaschcardRelationship
from .forms import StackForm, NewCardsForm
from .serializers import falshcard_serializer


@login_required(login_url='users:login')
def flashcards(request, stack_id):
    json_data = falshcard_serializer(stack_id, request)
    context = {'json_data': json_data, 'stack_id': stack_id}
    return render(request, 'flashcard/flashcards.html', context)


@login_required(login_url='users:login')
def edit_flashcards(request, stack_id):
    json_data = falshcard_serializer(stack_id, request)
    stack = Stack.objects.get(pk=stack_id)
    context = {'json_data': json_data, 'stack_id': stack_id, 'stack': stack}
    return render(request, 'flashcard/edit_flashcards.html', context)


def stack_list_view(request):
    stacks = Stack.objects.all().order_by('-created_at')
    context = {'stacks': stacks}
    return render(request, 'flashcard/stack_list.html', context)


@login_required(login_url='users:login')
def my_cards_view(request):
    user = request.user
    stacks = Stack.objects.filter(creator=user).order_by('-created_at')
    context = {'stacks': stacks}
    return render(request, 'flashcard/my_cards.html', context)


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


@login_required(login_url='users:login')
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

            return redirect('flashcard:edit_flashcards', stack_id=stack_id)
    else:
        form = NewCardsForm()
    
    context = {'form': form}
    return render(request, 'flashcard/add_new_cards.html', context)


def json_reciever(request):
    data = json.loads(request.body)

    if request.method == 'POST':
        stack_instance = get_object_or_404(Stack, pk=data['stack'])
        new_card = Flashcard.objects.create(term=data['term'], definition=data['definition'], stack=stack_instance)
        new_card.save()
        return JsonResponse({'message': 'Data received successfully', 'newCardId': new_card.id}, status=200)
    
    elif request.method == 'PUT':
        stack_id = data.get('stack_id')
        card_id = data.get('card_id')
        known = data.get('known')
        user = request.user

        if stack_id is not None:
            cards_to_reset = get_list_or_404(UserFlaschcardRelationship, user_id=user, flashcard_id__stack=stack_id)
            for card in cards_to_reset:
                card.reset_card()

        else:
            card_instance = get_object_or_404(Flashcard, pk=card_id)
            UserFlaschcardRelationship.change_known_or_create(user=user, card_instance=card_instance, true_or_false=known)

        return JsonResponse({'message': 'Data received successfully'}, status=200)
    
    elif request.method == 'DELETE':
        card_id = data.get('card_id')
        card_to_delete = get_object_or_404(Flashcard, pk=card_id)
        card_to_delete.delete()
        return JsonResponse({'message': 'Card deleted successfully'}, status=200)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
