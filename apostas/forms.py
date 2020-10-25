from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Aposta 


class CreateUserForm (UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class ApostaForm(ModelForm):
	class Meta:
		model = Aposta
		fields = '__all__'
		widgets = {
			'usuario' : forms.HiddenInput(),
			'partida' : forms.HiddenInput(),
			'time1Venceu' : forms.HiddenInput(),
			'time2Venceu' : forms.HiddenInput(),
			'empate' : forms.HiddenInput(),
		}