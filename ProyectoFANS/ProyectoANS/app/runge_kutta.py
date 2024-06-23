import matplotlib
matplotlib.use('Agg')  # Usar el backend 'Agg' para evitar problemas con el hilo principal

import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import sympy as sp
import pandas as pd

def runge_kutta_4(fx, x0, y0, h, aprox):
    x_vals = np.arange(x0, aprox + h, h) # Vector de valores de x desde x0 hasta aprox con paso h
    n = len(x_vals) # Cantidad de elementos en el vector x
    y = np.zeros(n) # Vector de soluciones y
    y[0] = y0 # Condición inicial para y
    
    # Convertir fx en una función lambda numérica
    x, y_sym = sp.symbols('x y')
    f = sp.lambdify((x, y_sym), fx, modules=['numpy'])

    # Crea un DataFrame para almacenar los resultados
    df = pd.DataFrame(columns=["Xi", "Yi", "k1", "k2", "k3", "k4", "Yi+1"])

    # Método de Runge-Kutta de orden 4
    for i in range(n - 1):
        k1 = f(x_vals[i], y[i]) # Evalúa f en (x[i], y[i])
        k2 = f(x_vals[i] + h / 2, y[i] + k1 * h / 2) # Evalúa f en (x[i] + h/2, y[i] + k1*h/2)
        k3 = f(x_vals[i] + h / 2, y[i] + k2 * h / 2) # Evalúa f en (x[i] + h/2, y[i] + k2*h/2)
        k4 = f(x_vals[i] + h, y[i] + k3 * h) # Evalúa f en (x[i] + h, y[i] + k3*h)
        y[i + 1] = y[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4) # Calcula y[i+1]
        df.loc[len(df)] = [x_vals[i], y[i], k1, k2, k3, k4, y[i + 1]] # Agrega los resultados al DataFrame

    # Grafica la solución aproximada
    fig, ax = plt.subplots()
    ax.plot(x_vals, y, label='Aproximada')
    ax.set(xlabel='x', ylabel='y', title='Runge-Kutta 4')
    ax.grid()
    ax.legend()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img = base64.b64encode(img.getvalue()).decode()
    # Retorna el DataFrame con los resultados y la imagen de la gráfica
    return df, img
