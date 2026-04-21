from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First name',
                'required': True,
                'minlength': '2',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last name',
                'required': True,
                'minlength': '2',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your message...',
                'required': True,
                'rows': 5,
                'minlength': '10',
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters.")
        return message
