from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # unique username
    def clean_username(self):
        get_username = self.cleaned_data.get('username')
        if User.objects.filter(username=get_username).exists():
            raise forms.ValidationError("Username already exists")
        return get_username
    
    # unique email
    def clean_email(self):
        get_email = self.cleaned_data.get('email')
        if User.objects.filter(email=get_email).exists():
            raise forms.ValidationError("Email already exists")
        return get_email