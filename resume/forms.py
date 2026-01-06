from django import forms
from django.contrib.auth.models import User
from .models import Application


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter', 'phone']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Write a brief cover letter...',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Your phone number',
                'class': 'form-control'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].help_text = 'Upload your resume (PDF, DOC, DOCX)'
        self.fields['phone'].help_text = 'We\'ll contact you on this number'