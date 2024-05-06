from django.forms import ModelForm

from .models import Stack


class StackForm(ModelForm):

    class Meta:
        model = Stack
        fields = ['stack_name']