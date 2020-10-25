from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ApostaForm
# Create your views here.


from .models import *
from .forms import CreateUserForm

#LOGOUT VIEW
def logoutUser(request):
	logout(request)
	return redirect('loginPage')

#LOGIN VIEW
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username = username, password = password)

		if user is not None:
			login(request, user)
			if user.is_superuser:
				return redirect('adminApostas')
			else:
				return redirect('home')
		else:
			messages.info(request, 'Username or password incorrect')

	context = {}
	return render (request, 'apostas/loginPage.html', context)

#PAGINA DE REGISTRO
def registerPage(request):
	#SE ELE ESTIVER LOGADO REDIRECTIONA PRA PAGINA INICIAL
	if request.user.is_authenticated:
		if request.user.is_superuser:
			return redirect('adminApostas')
		else:
			return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				#como o usuario é uma extensao do modelo original do user do django, temos que cria-lo manualmente
				#neste caso, coloquei esse create abaixo pra cada vez que for criado um user, criamos um usuario
				Usuario.objects.create(
					user=user,
					nome=user.username,
					email=user.email,
				)
				
				user = form.cleaned_data.get('username')
				messages.success(request, 'account was created for ' + user)
				return redirect('loginPage')

	context = {'form':form}
	return render (request, 'apostas/registerPage.html', context)

#A PARTIR DAQUI AS VIEWS TEM O DECORATOR LOGIN_REQUIRED, PARA QUE POSSAM ACESSAR SOMENTE SE ESTIVEREM LOGADAS
@login_required(login_url = 'loginPage')
def home(request):
	#pede os dados do usuario de acordo com a informacao de requisicao
	usuario = Usuario.objects.get(user=request.user)
	#pede as apostas de acordo com o usuario
	apostas_usuario = Aposta.objects.filter(usuario=usuario)
	context = {'usuario': usuario, 'apostas_usuario': apostas_usuario}
	return render (request, 'apostas/home.html', context)

@login_required(login_url = 'loginPage')
def fazerAposta(request, pk):
	fez_aposta = False
	#instancia um formulario de partida
	usuario = Usuario.objects.get(user=request.user)
	partida = Partida.objects.get(id=pk)
	apostas_usuario = Aposta.objects.filter(partida=pk).filter(usuario=usuario)

	formulario = ApostaForm(initial={'usuario': usuario, 'partida': partida})

	if apostas_usuario.filter(partida=pk).exists():
		fez_aposta = True

	if request.method == 'POST':
		print('Printing POST: ', request.POST)
		#instancia o formulario de partida com as informacoes que o usuario digitou
		formulario = ApostaForm(request.POST)
		#valida, salva o formulario e redireciona para a home
		if formulario.is_valid() and fez_aposta == False:
			usuario.saldo -= 5
			usuario.save()
			aposta = formulario.save()
			aposta.vencedorOuEmpate()
			aposta.save()
			return redirect('/')
	
	context = {'partida': partida, 'usuario': usuario, 'formulario': formulario, 'fez_aposta': fez_aposta}
	return render (request, 'apostas/fazerAposta.html', context)

@login_required(login_url = 'loginPage')
def partidasCadastradas(request):
	partidas = Partida.objects.all()
	usuario = Usuario.objects.get(user=request.user)
	context = {'partidas':partidas, 'usuario': usuario}
	return render (request, 'apostas/partidasCadastradas.html', context)


@login_required(login_url = 'loginPage')
def adminApostas(request):
	#aqui eu pretendo que pessoas com status de admin possam distribuir os premios da aposta
	apostas = Aposta.objects.all()
	partidas = Partida.objects.all()
	context = {'partidas':partidas,'apostas':apostas}
	return render (request, 'apostas/adminApostas.html', context)

#fiz isso mas nao sei se vai ser necessário
@login_required(login_url = 'loginPage')
def partidaApostasFeitas(request, pk):
	apostas_partida = Aposta.objects.filter(partida=pk)
	partida = Partida.objects.get(id=pk)
	context = {'apostas_partida':apostas_partida, 'partida': partida}
	return render (request, 'apostas/partidaApostasFeitas.html', context)

@login_required(login_url = 'loginPage')
def distribuirPremio(request, pk):	
	apostas_partida = Aposta.objects.filter(partida=pk)
	partida = Partida.objects.get(id=pk)

	qtdApostas = Aposta.objects.filter(partida=pk).count()
	contadorVencedores = 0
	contadorResultado = 0
	premio = 0

	for apostas in apostas_partida: 
		if (apostas.placar1 == partida.placar1 and apostas.placar2 == partida.placar2):
			print(apostas.usuario)
			contadorVencedores +=1
		elif (apostas.time1Venceu == partida.time1Venceu and apostas.time2Venceu == partida.time2Venceu):
			print(apostas.usuario)
			contadorResultado +=1
	print('Vencedores :', contadorVencedores)
	print('Resultado :', contadorResultado)
	if contadorVencedores > 0:
		premio = (qtdApostas * 5) / contadorVencedores
		print('Valor premio :', premio)
		for apostas in apostas_partida: 
			if (apostas.placar1 == partida.placar1 and apostas.placar2 == partida.placar2):
				usuario = Usuario.objects.get(nome=apostas.usuario)
				print('valor do saldo do cliente: ', usuario.saldo)
				usuario.saldo += premio
				print('valor do saldo do cliente junto c premio: ', usuario.saldo)
				usuario.save()
			apostas.delete()
	elif contadorResultado > 0: 
		premio = (qtdApostas * 5) / contadorResultado
		print('Valor premio :', premio)
		for apostas in apostas_partida: 
			if (apostas.time1Venceu == partida.time1Venceu and apostas.time2Venceu == partida.time2Venceu):
				usuario = Usuario.objects.get(nome=apostas.usuario)
				usuario.saldo += premio
				usuario.save()
			apostas.delete()
	else:
		for apostas in apostas_partida: 
			usuario = Usuario.objects.get(nome=apostas.usuario)
			usuario.saldo += 5
			usuario.save()
			apostas.delete()
	return redirect('adminApostas')
