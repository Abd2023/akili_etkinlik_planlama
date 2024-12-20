from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'date_of_birth', 'gender', 'phone_number', 'location', 'interests', 'profile_picture')

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'location', 'interests', 'profile_picture')
