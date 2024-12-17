from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome'}))
    endereco = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Endereço'}))
    cep = forms.CharField(label="", max_length=8, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CEP'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'endereco', 'cep', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
            super(UserRegisterForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'CPF (apenas números)'
            self.fields['username'].label = ''
            self.fields['username'].help_text = ''

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = ''

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar senha'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = ''
