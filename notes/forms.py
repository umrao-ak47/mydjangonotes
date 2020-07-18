from django import forms
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Note


class NewNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'body',)


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('confirm_password', 'Password does not match')
        return cd['confirm_password']
    
