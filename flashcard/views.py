import json
import itertools
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Flashcard, Stack, UserFlaschcardRelationship
from .forms import StackForm


def falshcard_serializer(stack_id, request):
    user = request.user.id
    queryset = Flashcard.objects.filter(stack=stack_id).order_by('id')
    queryset2 = UserFlaschcardRelationship.objects.filter(flashcard_id__stack=stack_id, user_id=user).order_by('flashcard_id__id')
    flashcards = list(queryset.values('term', 'definition', 'id'))
    flashcard_ids = list(queryset2.values('is_known', 'flashcard_id__id'))
    known_flashcard_ids = {card['flashcard_id__id'] for card in flashcard_ids if card['is_known']}

    transformed_flashcards = []
    for card in flashcards:
        known = card['id'] in known_flashcard_ids
        transformed_flashcards.append({
            'term': card['term'],
            'definition': card['definition'],
            'known': known
        })

    # json_data = []
    # for (entry, entry2) in itertools.zip_longest(serialized_data, serialized_data2):
    #     entry2 = {'flashcard_id__id': 0} if entry2 is None else entry2
    #     # print(entry, entry2)
    #     custom_entry = {
    #         'term': entry['term'],
    #         'definition': entry['definition'],
    #         "known":  entry2['is_known'] if entry['id'] == entry2['flashcard_id__id'] else False,
    #     }
    #     json_data.append(custom_entry)


    # json_data = []
    # for entry in serialized_data:
    #     for entry2 in serialized_data2:
    #         print(entry, entry2)
    #         custom_entry = {
    #             'term': entry['term'],
    #             'definition': entry['definition'],
    #             "known":  entry2['is_known'] if entry['id'] == entry2['flashcard_id__id'] and not None else pass,
    #         }
    #         json_data.append(custom_entry)

    json_data = json.dumps(transformed_flashcards)
    return json_data


def flashcards(request, pk):
    user = request.user
    json_data = falshcard_serializer(pk, request)
    context = {'json_data': json_data, 'pk': pk, 'user': user}
    return render(request, 'flashcard/flashcards.html', context)


def edit_flashcards(request, pk):
    json_data = falshcard_serializer(pk, request)
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
            form.instance.creator = request.user
            form.save()
            return redirect('flashcard:stack_list_view')
    else:
        form = StackForm()
    
    context = {'form': form}
    return render(request, 'flashcard/create_new_stack.html', context)


def json_new_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        stack_instance = Stack.objects.get(pk=data['stack'])
        Flashcard.objects.create(term=data['term'], definition=data['definition'], stack=stack_instance)
        return JsonResponse({'message': 'Data received successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
