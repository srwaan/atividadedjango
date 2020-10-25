from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('loginPage/', views.loginPage, name='loginPage'),
	path('registerPage/', views.registerPage, name='registerPage'),
	path('fazerAposta/<str:pk>', views.fazerAposta, name='fazerAposta'),
	path('partidasCadastradas/', views.partidasCadastradas, name='partidasCadastradas'),
	path('logout/', views.logoutUser, name='logout'),
	path('adminApostas/', views.adminApostas, name='adminApostas'),
	path('partidaApostasFeitas/<str:pk>', views.partidaApostasFeitas, name='partidaApostasFeitas'),
	path('distribuirPremio/<str:pk>', views.distribuirPremio, name='distribuirPremio'),
]