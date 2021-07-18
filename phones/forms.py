from django import forms
from django.contrib.auth.models import User

from phones.models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('name', 'last_name', 'phone_number')
        widgets = {
            'phone_number': forms.NumberInput
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
