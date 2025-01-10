import json
from random import shuffle

from .models import Flashcard, UserFlaschcardRelationship


def falshcard_serializer(stack_id, request, random_order = False):
    user = request.user.id
    queryset = Flashcard.objects.filter(stack=stack_id).order_by('-id')
    queryset2 = UserFlaschcardRelationship.objects.filter(flashcard_id__stack=stack_id, user_id=user).order_by('-flashcard_id__id')
    flashcards = list(queryset.values('term', 'definition', 'id'))
    flashcard_ids = list(queryset2.values('is_known', 'flashcard_id__id'))
    known_flashcard_ids = {card['flashcard_id__id'] for card in flashcard_ids if card['is_known']}

    transformed_flashcards = []
    for card in flashcards:
        known = card['id'] in known_flashcard_ids
        transformed_flashcards.append({
            'term': card['term'],
            'definition': card['definition'],
            'known': known,
            'id': card['id'],
        })

    if random_order:
        shuffle(transformed_flashcards)

    json_data = json.dumps(transformed_flashcards)
    return json_data
