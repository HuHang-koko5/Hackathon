from django import forms
from django.forms import widgets


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=15, min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True)
    widget = widgets.Textarea()

class RegisterUserForm(forms.Form):
    gender = (
        ('male', 'M'),
        ('female', 'F'),
    )
    username = forms.CharField(label="Username", max_length=15, min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    password1 = forms.CharField(label="Password", max_length=15, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)
    password2 = forms.CharField(label="Confirm", max_length=15, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)
    sex = forms.ChoiceField(label="Gender", choices=gender, required=True)
