from django import forms
from .models import CustomUser

class UpdateUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    password = forms.CharField(max_length=100)
    
    
class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'phone']
        widgets = {
            'password': forms.PasswordInput(),
        }


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'phone']
        widgets = {
            'password': forms.PasswordInput(),
        }


