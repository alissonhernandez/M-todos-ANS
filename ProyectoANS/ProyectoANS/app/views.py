from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
import numpy as np
from .hermite import *
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required
def view_profile(request):
    return render(request, 'profile.html', {'usuario': request.user})



# Create your views here.
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        pwd = request.POST.get('pwd')
        
        user = authenticate(request, username=usuario, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos.'})
    else:
        return render(request, 'login.html')
        

def user_register(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        
        if pwd1 == pwd2:
            try:
                user = User.objects.create_user(usuario, email, pwd1)
                user.save()
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'register.html', {'error': 'El usuario ya existe.'})
        else:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden.'})
    else:
        return render(request, 'register.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def hermite(request):
    if request.method == 'POST':
        cantidad_puntos = int(request.POST.get('cantidad_puntos'))
        datos_x = np.empty(cantidad_puntos)
        datos_fx = np.empty(cantidad_puntos)
        datos_fdx = np.empty(cantidad_puntos)
        for i in range(cantidad_puntos):
            datos_x[i] = float(request.POST.get(f'x-{i}'))
            datos_fx[i] = float(request.POST.get(f'fx-{i}'))
            datos_fdx[i] = float(request.POST.get(f'fdx-{i}'))

        z, d, df_hermite, df_txt = diferencias_divididas(datos_x, datos_fx, datos_fdx)
        pol, pasos = polinomio_hermite(d, z)
        df_hermite.insert(0, 'X', z)
        df_txt.insert(0, 'X', z)
        img = graficar_hermite(datos_x, datos_fx, pol)
        return render(request, 'hermite.html', {
            'resultado': True, 
            'img': img, 
            'df_hermite': df_hermite.to_html(), 
            'df_txt': df_txt.to_html(), 
            'polinomio': pol, 
            'pasos': pasos,
            'z': z, 
            'd': d
        })
    else:
        return render(request, 'hermite.html')

