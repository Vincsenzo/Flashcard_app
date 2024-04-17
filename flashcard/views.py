import json
from django.shortcuts import render
from django.http import JsonResponse

from .models import Flashcard, Stack


def flashcards(request, pk):
    queryset = Flashcard.objects.filter(stack=pk)
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
    context = {'json_data': json_data, 'pk': pk}
    return render(request, 'flashcard/flashcard.html', context)


def flashcard_list_view(request):
    stacks = Stack.objects.all()
    context = {'stacks': stacks}
    return render(request, 'flashcard/flashcard_list.html', context)


def json_request_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        stack_instance = Stack.objects.get(pk=data['stack']) # TODO: fix this
        Flashcard.objects.create(term=data['term'], definition=data['definition'], stack=stack_instance)
        return JsonResponse({'message': 'Data received successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
