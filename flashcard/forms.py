from django.forms import ModelForm, Form
from django import forms

from .models import Stack


class StackForm(ModelForm):

    class Meta:
        model = Stack
        fields = ['stack_name']


class NewCardsForm(Form):
    new_cards = forms.CharField(widget=forms.Textarea())

    class Meta:
        fields = ['new_cards']