import json
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Flashcard, Stack
from .forms import StackForm


def falshcard_serializer(stack_id):
    queryset = Flashcard.objects.filter(stack=stack_id)
    serialized_data = list(queryset.values('term', 'definition'))

    json_data = []
    for entry in serialized_data:
        custom_entry = {
            'term': entry['term'],
            'definition': entry['definition'],
            "known": False,
        }
        json_data.append(custom_entry)

    json_data = json.dumps(json_data)
    return json_data


def flashcards(request, pk):
    json_data = falshcard_serializer(pk)
    context = {'json_data': json_data, 'pk': pk}
    return render(request, 'flashcard/flashcards.html', context)


def edit_flashcards(request, pk):
    json_data = falshcard_serializer(pk)
    context = {'json_data': json_data, 'pk': pk}
    return render(request, 'flashcard/edit_flashcards.html', context)


def stack_list_view(request):
    stacks = Stack.objects.all()
    context = {'stacks': stacks}
    return render(request, 'flashcard/stack_list.html', context)


def create_new_stack(request):
    if request.method == 'POST':
        form = StackForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('flashcard:stack_list_view')
    else:
        form = StackForm()
    
    context = {'form': form}
    return render(request, 'flashcard/create_new_stack.html', context)


def json_request_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        stack_instance = Stack.objects.get(pk=data['stack'])
        Flashcard.objects.create(term=data['term'], definition=data['definition'], stack=stack_instance)
        return JsonResponse({'message': 'Data received successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
