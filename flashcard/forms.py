from django import forms

from .models import Stack


class StackForm(forms.ModelForm):

    class Meta:
        model = Stack
        fields = '__all__'