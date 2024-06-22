# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('hermite/', views.hermite, name='hermite'),
    path('runge_kutta/', views.runge_kutta_view, name='runge_kutta'),
]