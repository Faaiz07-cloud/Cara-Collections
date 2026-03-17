from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile, Contact
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'gender', 'profile_pic']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Enter your registered email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered!")
        return email       

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}), strip=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}), strip= False)

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if not new_password1 or not new_password2:
            raise forms.ValidationError("Both password fields are required!")
        if new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match! Please re-enter.")
        if len(new_password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long!")
        
        return new_password2
    
class ContactForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'input-field',
        }))    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'input-field',
        }))

    class Meta:
        model = Contact
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Enter your subject', 'class': 'input-field',}),
            'message': forms.Textarea(attrs={'placeholder': 'Enter your message', 'class': 'input-field',}),
        }  

    # validations
    def clean(self):
        cleaned_data = super().clean() 
        username = self.cleaned_data.get('username')   
        email = self.cleaned_data.get('email')  

        if not User.objects.filter(username=username, email=email).exists():
          raise forms.ValidationError('Username or Email is incorrect!')
            
        return cleaned_data     