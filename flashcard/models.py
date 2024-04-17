from django.db import models
from django.contrib.auth.models import User


class Stack(models.Model):
    stack_name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.stack_name


class Flashcard(models.Model):
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE)
    term = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.term} - {self.definition}'
