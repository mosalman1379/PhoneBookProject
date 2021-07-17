from django import forms
from phones.models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('name', 'last_name', 'phone_number')
        widgets = {
            'phone_number': forms.NumberInput
        }
