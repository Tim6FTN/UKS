from django import forms
from django.forms import ModelForm, TextInput
from label.models import Label


class LabelForm(ModelForm):

    class Meta:
        model = Label
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'})
        }
