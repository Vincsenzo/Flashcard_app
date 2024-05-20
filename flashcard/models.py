from django.db import models
from django.contrib.auth.models import User


class Stack(models.Model):
    stack_name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


    # def reset_stack(self):
    #     cards = Flashcard.objects.filter(stack=self) #TODO: mak this work
    #     for card in cards:
    #         card.

    def __str__(self):
        return self.stack_name


class Flashcard(models.Model):
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE)
    term = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.id} | {self.term} - {self.definition}'
    

class UserFlaschcardRelationship(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard_id = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    is_known = models.BooleanField(default=False)


    def change_known(self):
        self.is_known = not self.is_known
        self.save()

    
    def reset_card(self):
        self.is_known = False
        self.save()


    def __str__(self):
        return f'{self.user_id.username} | {self.flashcard_id.term} | {self.is_known}'
