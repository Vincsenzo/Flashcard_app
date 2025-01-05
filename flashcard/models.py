from django.db import models
from django.contrib.auth.models import User


class Stack(models.Model):
    stack_name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stack_name


class Flashcard(models.Model):
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE)
    term = models.CharField(max_length=500)
    definition = models.CharField(max_length=400)

    def __str__(self):
        return f'{self.id} | {self.term} - {self.definition}'
    

class UserFlaschcardRelationship(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard_id = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    is_known = models.BooleanField(default=False)

    @classmethod
    def change_known_or_create(cls, user, card_instance, true_or_false: bool):
        obj, created = cls.objects.update_or_create(
            user_id=user,
            flashcard_id=card_instance,
            defaults={'is_known': true_or_false}
        )
        return obj

    def reset_card(self):
        self.is_known = False
        self.save()

    def __str__(self):
        return f'{self.user_id.username} | {self.flashcard_id.term} | {self.is_known}'
