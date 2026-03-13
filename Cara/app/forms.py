from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    last_name = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class':'form-control form-control-lg'}))
    username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg'}), strip=False)   
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg'}), strip=False)   

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    # unique username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists!')
        else:
            return username     
        
    # unique email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists!')
        else:
            return email  

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password1 or not password2:
            raise forms.ValidationError("Both password fields are required!")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match! Please re-enter.")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long!")
        
        return password2      
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg'}), strip=False) 

    def clean_username(self): 
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist.")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')   
        password = self.cleaned_data.get('password')

        if username and User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect Password!")
        return password          