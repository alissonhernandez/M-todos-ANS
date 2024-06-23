from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import numpy as np
import sympy as sp
from .hermite import *
from .runge_kutta import *
import pandas as pd
# Importa la funcion latex de sympy
from sympy import symbols, sqrt, sin, cos, tan, exp, pi, E, latex


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

def runge_kutta(request):
    if request.method == 'POST':
        fx = request.POST.get('fx')
        x0 = float(request.POST.get('x0'))
        y0 = float(request.POST.get('y0'))
        h = float(request.POST.get('h'))
        aprox = float(request.POST.get('aprox'))

        # Reemplaza funciones exponenciales por las de SymPy
        fx = fx.replace('^', '**')
        fx = fx.replace('e', str(sp.E))

        # Define un diccionario con todas las funciones matemáticas necesarias
        local_dict = {
            'sqrt': sqrt,
            'sin': sin,
            'cos': cos,
            'tan': tan,
            'exp': exp,
            'pi': pi,
            'e': E
        }

        # Valida que la función sea correcta
        try:
            x, y = symbols('x y')
            fx = sp.sympify(fx, locals=local_dict)
        except Exception as e:
            return render(request, 'runge_kutta.html', {'error': f'La función ingresada no es válida: {e}'})
        
        # Calcula la solución aproximada con el método de Runge-Kutta de orden 4
        df_rk, img = runge_kutta_4(fx, x0, y0, h, aprox)
        
        # Crea un DataFrame con las columnas Xi-1 y Yi-1
        df = df_rk.copy()

        # Recorre el DataFrame, agrega una nueva columna Xi-1 y una Yi-1 siempre que i sea mayor a 0
        for i in range(1, len(df)):
            df.loc[i, 'Xim1'] = df.loc[i - 1, 'Xi']
            df.loc[i, 'Yip1'] = df.loc[i - 1, 'Yi+1']
        # Convierte el DataFrame a un diccionario de registros
        df = df.to_dict('records') # Convierte el DataFrame a un diccionario de registros
        fx_latex = latex(fx)
        # Retorna el DataFrame con los resultados y la imagen de la gráfica
        return render(request, 'runge_kutta.html', {
            'resultado': True,
            'img': img,
            'df_rk': df_rk.to_html(),
            'df': df,
            'fx_latex': fx_latex,
            'h': h,
        })
    else:
        return render(request, 'runge_kutta.html')
