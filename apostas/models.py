from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Usuario (models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	nome = models.CharField(max_length=200, null=True)
	telefone = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=200, null=True)
	saldo = models.IntegerField(default=10, null=True)
	data_criacao = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.nome

class Partida (models.Model):
	time1 = models.CharField(max_length=50, null=True)
	time2 = models.CharField(max_length=50, null=True)
	placar1 = models.IntegerField(default=0)
	placar2 = models.IntegerField(default=0)
	data_partida = models.DateTimeField(auto_now_add=True, null=True)
	time1Venceu = models.BooleanField(default=False)
	time2Venceu = models.BooleanField(default=False)
	empate = models.BooleanField(default=False)

	def __str__(self):
		return self.time1 +" x "+ self.time2

class Aposta(models.Model):
	usuario = models.ForeignKey(Usuario, null=True, on_delete=models.CASCADE)
	partida = models.ForeignKey(Partida, null=True, on_delete=models.CASCADE)
	placar1 = models.IntegerField(default=0)
	placar2 = models.IntegerField(default=0)
	data_criacao = models.DateTimeField(auto_now_add=True, null=True)
	time1Venceu = models.BooleanField(default=False)
	time2Venceu = models.BooleanField(default=False)
	empate = models.BooleanField(default=False)
	
	def vencedorOuEmpate(self):
		if self.placar1 > self.placar2:
			self.time1Venceu = True
		elif self.placar1 < self.placar2:
			self.time2Venceu = True
		else: 
			self.empate = True;

	def __str__(self):
		return "Aposta de "+ self.usuario.nome
