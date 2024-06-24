from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # RUTAS DE GESTION DE USUARIOS
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('perfil/', views.view_profile , name='profile'),
    path('history/', views.view_history, name='history'),
    # RUTAS DE DIRECCIONAMIENTO DE LA CALCULADORA
    path('hermite/', views.hermite, name='hermite'),
    path('runge-kutta/', views.runge_kutta, name='runge_kutta'),
]
