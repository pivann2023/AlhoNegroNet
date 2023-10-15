from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import *



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Obrigatório. Informe um endereço de e-mail válido.',label='E-mail')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class EstufaForm(forms.ModelForm):
    class Meta:
         model = estufa
         exclude = ['created_at','modified_at']

class LoteForm(forms.ModelForm):
    class Meta:
         model = lote
         exclude = ['estufa']