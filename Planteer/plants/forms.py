from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Plant name',
                'required': True,
                'minlength': '2',
            }),
            'about': forms.Textarea(attrs={
                'placeholder': 'Describe the plant...',
                'required': True,
                'rows': 4,
            }),
            'used_for': forms.Textarea(attrs={
                'placeholder': 'What is this plant used for?',
                'required': True,
                'rows': 3,
            }),
            'category': forms.Select(attrs={
                'required': True,
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Plant name must be at least 2 characters.")
        return name
