from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # RUTAS DE GESTION DE USUARIOS
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    # RUTAS DE DIRECCIONAMIENTO DE LA CALCULADORA
    path('hermite/', views.hermite, name='hermite'),
]